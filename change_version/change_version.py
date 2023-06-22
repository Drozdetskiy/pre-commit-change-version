import re

from git import Repo
from semantic_version import Version as BaseVersion


class Version(BaseVersion):
    def next_prerelease(self):
        if self.prerelease:
            if isinstance(self.prerelease, tuple):
                return Version(
                    major=self.major,
                    minor=self.minor,
                    patch=self.patch,
                    prerelease=(
                        self.prerelease[0], str(int(self.prerelease[1]) + 1)
                    ),
                )
            else:
                raise Exception("Unsupported prerelease format")

        return Version(
            major=self.major,
            minor=self.minor,
            patch=self.patch,
            prerelease=("beta", "1"),
        )


VERSION_REGEXP = re.compile('version = "(\\d+.\\d+.\\d+)(-beta.\\d+)*"')


def main() -> None:
    repo = Repo()
    result = VERSION_REGEXP.findall(
        repo.git.diff(
            "HEAD~1",
            "pyproject.toml",
        )
    )
    if not result:
        with open("pyproject.toml") as f:
            lines = f.readlines()

            for i in range(len(lines)):
                line = lines[i]
                result = VERSION_REGEXP.findall(line)

                if result:
                    new_version = Version("".join(result[0])).next_prerelease()
                    lines[i] = f'version = "{new_version}"\n'
                    break
            else:
                raise Exception("Version not found in pyproject.toml")

        with open("pyproject.toml", "w") as f:
            f.writelines(lines)

        raise SystemExit(
            "Please add bumped version to commit or "
            "fix version in pyproject.toml manually",
        )


if __name__ == "__main__":
    main()
