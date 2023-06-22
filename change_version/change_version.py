import re
import toml

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
                    prerelease=(self.prerelease[0], str(int(self.prerelease[1]) + 1)),
                )
            else:
                raise Exception("Unsupported prerelease format")

        return Version(
            major=self.major,
            minor=self.minor,
            patch=self.patch,
            prerelease=("beta", "1"),
        )


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
        with open("pyproject.toml", "wb") as f:
            data = toml.load(f)
            version = data["project"]["version"]
            data["project"]["version"] = str(Version(version).next_prerelease())
            toml.dump(data, f)

        raise SystemExit(
            "Please add bumped version to commit or "
            "fix version in pyproject.toml manually",
        )


if __name__ == "__main__":
    main()
