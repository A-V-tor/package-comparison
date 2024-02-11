
import requests
from dataclasses import dataclass, asdict
import pandas as pd
import click
import concurrent.futures


def parse_version(version: str) -> list:
    version_components = version.split('.')
    version_numbers = [component for component in version_components if component.isdigit()]
    return version_numbers


@dataclass
class Package:
    name: str
    epoch: int
    version: str
    release: str
    arch: str
    disttag: str
    buildtime: int
    source: str

    def __eq__(self, other):
            return isinstance(other, Package) and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash((self.name, self.epoch, self.version, self.release, self.arch, self.disttag, self.buildtime, self.source))



def make_request(url) -> set[Package]:
    res = requests.get(url)
    res_json = res.json().get('packages')
    name_space = set()
    if res_json is None:
        raise TypeError("Check the branch name")

    for dictpackege in res_json:
        p = Package(**dictpackege)
        if p not in name_space:
            name_space.add(p)

    return name_space


@click.command()
@click.argument('branch')
@click.argument('branch2')
def main(branch, branch2):
    URL = 'https://rdb.altlinux.org/api/export/branch_binary_packages/'
    with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(make_request, URL + branch)
            future2 = executor.submit(make_request, URL + branch2)

            result1 = future1.result()
            result2 = future2.result()

    first_branch_intersection = result1.intersection(result2)
    second_branch_intersection = result2.intersection(result1)

    # Преобразуем список объектов в DataFrame
    df = pd.DataFrame([asdict(package) for package in result1])
    df2 = pd.DataFrame([asdict(package) for package in result2])

    # объединение для сравнивания версий
    merged_df = pd.merge(df, df2, on='name', suffixes=('_sisyphus', '_p10'))

    filtered_df = merged_df[
        merged_df.apply(lambda row: parse_version(row['version_sisyphus']) > parse_version(row['version_p10']), axis=1)
    ]

    _ = filtered_df.filter(like='_sisyphus')
    _ = _.rename(columns=lambda x: x.replace('_sisyphus', ''))

    version_release_difference = _.to_dict(orient='records')

    result_dict = {
        "sisyphus_intersection": first_branch_intersection,
        "p10_intersection": second_branch_intersection,
        "great-version-release": version_release_difference,
    }
    click.echo(result_dict)


if __name__ == '__main__':
    main()
