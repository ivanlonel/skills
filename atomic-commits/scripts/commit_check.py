#!/usr/bin/env python3
"""Check a draft commit message or a pull request's size.

Run it on your own draft before `git commit`. It is a check, not a hook.

  python3 commit_check.py message FILE [--lang pt-BR|en] [--types a,b]
                                       [--no-cc] [--emoji] [--case lower|upper|any]
  python3 commit_check.py pr-size BASE [--limit 150000]
  python3 commit_check.py --self-test

Exit status: 0 = no errors (warnings can exist), 1 = errors, 2 = usage error.
"""
import argparse
import re
import subprocess
import sys
import unicodedata

DEFAULT_TYPES = ("feat fix docs test build perf style refactor chore ci raw "
                 "cleanup remove init revert security").split()
TITLE_SOFT, TITLE_HARD, BODY_HARD = 50, 72, 72
TRAILING_PUNCT = ".,;:!?…"
EMOJI = r"(?::[a-z0-9_+-]+:|[^\x00-\x7f]+)"
CC_TITLE = re.compile(
    r"^(?:(?P<emoji>" + EMOJI + r")\s+)?(?P<type>[A-Za-z]+)"
    r"(?:\((?P<scope>[^()]*)\))?(?P<bang>!)?: (?P<desc>\S.*)$")
TRAILER = re.compile(r"^(?P<token>[A-Za-z0-9][A-Za-z0-9-]*): \S")
HASH_TRAILER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]* #\S")
URL = re.compile(r"https?://\S+")
URL_ONLY = re.compile(r"^\s*<?https?://\S+>?\s*$")
REF_LINE = re.compile(r"^\s*\[\d+\]:?\s+\S+://\S+\s*$")
CLOSING = re.compile(r"^(close[sd]?|fix(e[sd])?|resolve[sd]?): https://github\.com/",
                     re.IGNORECASE)


def width(text):
    """Display columns. Wide chars and emoji presentation = 2, marks = 0."""
    # ponytail: East Asian Width + U+FE0F only; ZWJ sequences and flags
    # over-count. Use a grapheme library if repos start using those.
    cols = 0
    for i, ch in enumerate(text):
        if unicodedata.category(ch) in ("Mn", "Me", "Cf") or 0xFE00 <= ord(ch) <= 0xFE0F:
            continue
        wide = unicodedata.east_asian_width(ch) in ("W", "F")
        emoji_vs = i + 1 < len(text) and text[i + 1] == "️"
        cols += 2 if wide or emoji_vs else 1
    return cols


def first_word_ok_pt(desc):
    words = desc.split()
    if words and words[0].lower() == "não":
        words = words[1:]
    if not words:
        return False
    word = words[0].strip("`\"'").lower()
    if "-" in word:  # enclitic: torná-lo, removê-la, defini-las
        head = word.split("-")[0]
        return head.endswith("r") or head[-1:] in "áêíô"
    return word.endswith("r")


def check_message(text, lang=None, types=DEFAULT_TYPES, cc=True, emoji=False,
                  case="lower"):
    """Return (errors, warnings) for one commit message."""
    errors, warnings = [], []
    if text.startswith("﻿"):
        errors.append("file starts with a UTF-8 BOM: write it without a BOM")
        text = text[1:]
    lines = [line.rstrip("\r") for line in text.split("\n")]
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines or not lines[0].strip():
        return ["the title (line 1) is empty"], warnings
    title = lines[0]

    # Title width
    cols = width(title)
    exempt = bool(URL.search(title) or "`" in title)
    if cols > TITLE_HARD:
        msg = "title is %d columns (max %d)" % (cols, TITLE_HARD)
        (warnings if exempt else errors).append(
            msg + (": allowed only if the URL/code must be in the title" if exempt else ""))
    elif cols > TITLE_SOFT:
        warnings.append("title is %d columns (target %d): shorten it if you can"
                        % (cols, TITLE_SOFT))
    if re.search(r"(^|\s)\(?#\d+\)?(\s|$)", title):
        errors.append("issue reference in the title: move it to a footer")

    desc = title
    bang = False
    if cc:
        m = CC_TITLE.match(title)
        if not m:
            errors.append("title is not `type(scope)!: description`")
        else:
            desc, bang = m.group("desc"), bool(m.group("bang"))
            if m.group("emoji") and not emoji:
                errors.append("emoji prefix: use it only when the repo history does (--emoji)")
            if emoji and not m.group("emoji"):
                warnings.append("the repo uses an emoji prefix, but this title has none")
            if m.group("type") not in types:
                errors.append("type %r is not one of: %s" % (m.group("type"), ", ".join(types)))
            scope = m.group("scope")
            if scope is not None:
                if not re.fullmatch(r"[a-zA-Z0-9_./-]+", scope):
                    errors.append("scope %r: use only letters, digits, _ . / -" % scope)
                elif scope != scope.lower():
                    warnings.append("scope %r is not lowercase" % scope)
    if desc[-1:] in TRAILING_PUNCT:
        errors.append("title ends with punctuation %r" % desc[-1])
    first = desc.lstrip("`\"'")[:1]
    if case == "lower" and first.isupper():
        warnings.append("description starts uppercase: OK only for a proper noun "
                        "or identifier")
    elif case == "upper" and first.islower():
        warnings.append("description starts lowercase, but the repo capitalizes")
    if lang == "pt-BR":
        if not first_word_ok_pt(desc):
            errors.append("description must start with an infinitive (or 'não' + "
                          "infinitive): 'Se aplicado, este commit irá <descrição>'")
        if " e " in desc:
            warnings.append("' e ' in the title: if it joins two actions, split the commit")
    elif lang == "en":
        verb = desc.split()[0].lower() if desc.split() else ""
        if verb.endswith(("ed", "ing")):
            warnings.append("first word %r: use the imperative ('If applied, this "
                            "commit will <description>')" % verb)
        if " and " in desc:
            warnings.append("' and ' in the title: if it joins two actions, split the commit")

    # Body and footers
    if len(lines) > 1 and lines[1].strip():
        errors.append("line 2 must be blank")
    fenced = False
    for n, line in enumerate(lines[1:], start=2):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        cols = width(line)
        if cols <= BODY_HARD or fenced or line.startswith(("    ", "\t")):
            continue
        if URL_ONLY.match(line) or REF_LINE.match(line):
            continue
        if URL.search(line) or "`" in line:
            warnings.append("line %d is %d columns: allowed only for an unsplittable "
                            "URL/code" % (n, cols))
        else:
            errors.append("line %d is %d columns (max %d)" % (n, cols, BODY_HARD))

    paragraphs, current = [], []
    for line in lines[2:]:
        if line.strip():
            current.append(line)
        elif current:
            paragraphs.append(current)
            current = []
    if current:
        paragraphs.append(current)
    if any(re.match(r"^BREAKING CHANGE:", line) for line in lines[1:]):
        errors.append("use `BREAKING-CHANGE:` (hyphen): Git does not parse a token "
                      "with a space, and drops the whole trailer block")
    trailers = []
    last = paragraphs[-1] if paragraphs else []
    if any(TRAILER.match(line) or HASH_TRAILER.match(line) for line in last):
        for line in last:
            match = TRAILER.match(line)
            if match:
                trailers.append(match.group("token"))
            elif line[:1] in (" ", "\t"):
                continue
            elif HASH_TRAILER.match(line):
                errors.append("footer %r: write `Token: value` (Git does not parse "
                              "`Token #value`)" % line)
            else:
                errors.append("line %r breaks the trailer block: keep only "
                              "`Token: value` lines (indent continuations)" % line)
            if CLOSING.match(line):
                warnings.append("GitHub documents `Closes: #N`, not URLs: use #N "
                                "(or owner/repo#N)")
    if cc:
        has_breaking = "BREAKING-CHANGE" in trailers
        if bang and not has_breaking:
            errors.append("title has `!`: add a `BREAKING-CHANGE: <summary>` footer")
        if has_breaking and not bang:
            errors.append("BREAKING-CHANGE footer: add `!` before the colon in the title")
        m = CC_TITLE.match(title)
        if m and m.group("type") == "revert" and "Refs" not in trailers:
            warnings.append("revert: add a `Refs: <sha>` footer")
    return errors, warnings


def cmd_message(args):
    try:
        with open(args.file, encoding="utf-8") as handle:
            text = handle.read()
    except UnicodeDecodeError:
        print("ERROR: the file is not valid UTF-8")
        return 1
    types = [t.strip() for t in args.types.split(",")] if args.types else DEFAULT_TYPES
    errors, warnings = check_message(text, args.lang, types, not args.no_cc,
                                     args.emoji, args.case)
    for warning in warnings:
        print("WARN: " + warning)
    for error in errors:
        print("ERROR: " + error)
    print("FAIL" if errors else "OK")
    return 1 if errors else 0


def cmd_pr_size(args):
    # Plain `git diff` shows binaries as one "Binary files differ" line,
    # so they are excluded in practice.
    result = subprocess.run(
        ["git", "-c", "core.quotePath=false", "diff", "--no-color", "--no-ext-diff",
         "--no-textconv", args.base + "...HEAD"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        print("ERROR: " + result.stderr.decode("utf-8", "replace").strip())
        return 2
    size = len(result.stdout.decode("utf-8", "replace"))
    print("PR diff: %d characters (limit %d)" % (size, args.limit))
    if size >= args.limit:
        print("OVER: split it into atomic PRs, or explain in the PR body why it cannot be split")
        return 1
    return 0


def self_test():
    ok = "fix(pedidos): multiplicar preço pela quantidade\n"
    assert check_message(ok, "pt-BR") == ([], []), check_message(ok, "pt-BR")
    assert width("✨") == 2 and width("á") == 1 and width("á") == 1
    assert width("♻️") == 2 and width("abc") == 3
    long_title = "fix: " + "a" * 70
    assert check_message(long_title)[0], "72+ title must fail"
    assert not check_message("fix: " + "a" * 50)[0], "51-72 title is a warning only"
    assert check_message("fix: " + "a" * 50)[1]
    errors, warnings = check_message("fix(auth): Adicionar login.", "pt-BR")
    assert any("punctuation" in e for e in errors) and warnings
    assert check_message("feat: adicionando login", "pt-BR")[0]
    assert check_message("feat: atualização do login", "pt-BR")[0]
    for desc in ("torná-lo opcional", "não exigir token", "pôr cache", "definir `X`"):
        assert not check_message("feat: " + desc, "pt-BR")[0], desc
    breaking_space = "feat!: remover rota v1\n\nBREAKING CHANGE: rota removida\n"
    assert any("hyphen" in e for e in check_message(breaking_space)[0])
    assert check_message("feat!: remover rota v1\n")[0], "! needs a footer"
    good_breaking = ("feat(api)!: remover rotas v1\n\nUse `/v2/orders`.\n\n"
                     "BREAKING-CHANGE: rotas v1 removidas\nCloses: #142\n")
    assert check_message(good_breaking, "pt-BR") == ([], []), check_message(good_breaking, "pt-BR")
    assert check_message("✨ feat: adicionar csv")[0]
    assert not check_message("✨ feat: adicionar csv", emoji=True)[0]
    assert check_message("wip: algo")[0], "unknown type"
    assert not check_message("wip: algo", types=["wip"])[0]
    assert check_message("fix: corrigir total (#12)")[0], "issue ref in title"
    body = "fix: corrigir total\n\n" + "palavra " * 10 + "\n"
    assert check_message(body)[0], "body line over 72"
    url_body = "fix: corrigir total\n\nVer:\n\nhttps://example.com/" + "a" * 90 + "\n"
    assert not check_message(url_body)[0]
    assert check_message("﻿fix: corrigir total\n")[0], "BOM"
    assert check_message("fix: corrigir total\ncorpo\n")[0], "line 2 must be blank"
    mixed = "fix: corrigir total\n\nCloses: #1\ntexto solto\n"
    assert check_message(mixed)[0], "mixed trailer block"
    assert check_message("fix: corrigir total\n\nRefs #1\nCloses: #2\n")[0]
    assert check_message("fix: corrigir total\n\nRefs #142\n")[0], "lone hash footer"
    gh = "fix: corrigir total\n\nCloses: https://github.com/o/r/issues/1\n"
    assert check_message(gh)[1] and not check_message(gh)[0]
    assert not check_message("Corrigir total do pedido", cc=False, case="upper")[0]
    print("self-test passed")
    return 0


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="replace")
    if argv is None:
        argv = sys.argv[1:]
    if argv == ["--self-test"]:
        return self_test()
    parser = argparse.ArgumentParser(description="Check a commit message or a PR's size.")
    sub = parser.add_subparsers(dest="command")
    msg = sub.add_parser("message", help="check a draft commit message file")
    msg.add_argument("file")
    msg.add_argument("--lang", choices=["pt-BR", "en"],
                     help="enable the verb-form check for this language")
    msg.add_argument("--types", help="comma-separated type list from the repo convention")
    msg.add_argument("--no-cc", action="store_true",
                     help="the repo does not use Conventional Commits")
    msg.add_argument("--emoji", action="store_true", help="the repo uses an emoji prefix")
    msg.add_argument("--case", choices=["lower", "upper", "any"], default="lower",
                     help="first letter of the description (repo convention)")
    size = sub.add_parser("pr-size", help="count the characters of BASE...HEAD")
    size.add_argument("base", help="for example origin/main")
    size.add_argument("--limit", type=int, default=150000)
    args = parser.parse_args(argv)
    if args.command == "message":
        return cmd_message(args)
    if args.command == "pr-size":
        return cmd_pr_size(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
