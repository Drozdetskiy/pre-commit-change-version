import re
import subprocess

from git import Repo

VERSION_REGEXP = re.compile('version = "\\d+.\\d+.\\d+b\\d+"')


def main() -> None:
    repo = Repo()
    result = VERSION_REGEXP.findall(
        repo.git.diff(
            "HEAD~1",
            "pyproject.toml",
        )
    )
    if not result:
        p = subprocess.Popen(
            "pdm bump pre-release --pre beta", stdout=subprocess.PIPE, shell=True
        )
        result_message, *_ = p.communicate()

        for line in result_message.split("\n"):
            print(line)

        raise SystemExit(
            "Please add bumped version to commit or "
            "fix version in pyproject.toml manually",
        )


if __name__ == "__main__":
    main()
