from version_utils import rpm
from version_utils.errors import RpmError
import requests
from dataclasses import dataclass
import click
import concurrent.futures
from simple_term_menu import TerminalMenu
from tabulate import tabulate
from tqdm import tqdm


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
        return hash(
            (
                self.name,
                self.epoch,
                self.version,
                self.release,
                self.arch,
                self.disttag,
                self.buildtime,
                self.source,
            )
        )


def make_request(url) -> dict[str:Package]:
    try:
        res = requests.get(url, timeout=10)
    except TimeoutError:
        raise KeyboardInterrupt('Server is not responding')

    # проверка что ответ с данными
    if str(res.status_code)[0] != '2':
        raise ValueError('Incorrect server response')

    res_json = res.json().get('packages')
    name_space = dict()
    if res_json is None:
        raise TypeError('Check the branch name')

    for dictpackage in res_json:
        p = Package(**dictpackage)
        if p not in name_space:
            name_space[p.name] = p

    return name_space


@click.command()
@click.argument('branch')
@click.argument('branch2')
def main(branch, branch2):
    URL = 'https://rdb.altlinux.org/api/export/branch_binary_packages/'
    with tqdm(total=60) as pbar:
        pbar.update(10)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(make_request, URL + branch)
            future2 = executor.submit(make_request, URL + branch2)

            result1 = future1.result()
            pbar.update(15)
            result2 = future2.result()
            pbar.update(15)

        first_branch_difference = set(result1.values()).difference(
            set(result2.values())
        )
        second_branch_difference = set(result2.values()).difference(
            set(result1.values())
        )
        pbar.update(10)

        version_release_difference = set()

        error_packages = 0
        for package in result1.values():
            if package.name in result2:
                first_package_compared = f'{package.name}-{package.version}-{package.release}.{package.arch}'
                package_2 = result2[package.name]
                second_package_compared = f'{package_2.name}-{package_2.version}-{package_2.release}.{package_2.arch}'

                try:
                    res = rpm.compare_packages(
                        first_package_compared, second_package_compared
                    )

                    # если версия из 1 ветки больше, то ее добавляем в результат
                    if res == 1:
                        version_release_difference.add(package)

                except RpmError:
                    error_packages += 1

        pbar.update(10)

        result_dict = {
            'first_branch_difference': first_branch_difference,
            'second_branch_difference': second_branch_difference,
            'version_release_difference': version_release_difference,
            'error': error_packages,
        }

        options = [
            'first_branch_difference',
            'second_branch_difference',
            'version_release_difference',
        ]
        terminal_menu = TerminalMenu(options)

        while True:
            menu_entry_index = terminal_menu.show()

            # Обработка выхода из меню
            if menu_entry_index is None:
                break

            # Получаем выбранное значение
            selected_value = result_dict[options[menu_entry_index]]
            click.echo_via_pager(
                tabulate(
                    [
                        [i.name, i.version, i.release, i.arch, i.source]
                        for i in selected_value
                    ],
                    headers=['name', 'version', 'release', 'arch', 'source'],
                )
            )


if __name__ == '__main__':
    main()
