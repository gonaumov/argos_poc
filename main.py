from re import search, IGNORECASE, sub
from pathlib import Path

from argostranslate.translate import Language, package, get_installed_languages


def find_language(input_code: str, language_list: list[Language]) -> Language:
    try:
        return [language for language in language_list if language.code == input_code][0]
    except:
        print('Cannot find installed language')


def write_data_to_file(input_file_path: str, input_data: str):
    with open(input_file_path, 'a', encoding='windows-1252') as output_file:
        output_file.write(input_data)


def translate_files(from_code: str, to_code: str):
    # Download and install Argos Translate package
    package.update_package_index()
    available_packages = package.get_available_packages()
    available_package = list(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )[0]

    download_path = available_package.download()
    package.install_from_path(download_path)

    # Translate
    installed_languages = get_installed_languages()

    from_lang = find_language(from_code, installed_languages)

    to_lang = find_language(to_code, installed_languages)

    translation = from_lang.get_translation(to_lang)

    p = Path('.')

    text_files = [x.name for x in p.iterdir() if x.is_file() and search(r'\.txt$', x.name, IGNORECASE)]

    for file_path in text_files:
        with open(file_path, 'r', encoding='utf-8') as input_file:
            translated_text = translation.translate(input_file.read())
            file_name = sub(r'\.txt$', '', file_path)
            write_data_to_file(f'{file_name}_translation_result.txt', translated_text)

    print(f'All done. {len(text_files)} files were translated!')


print('Translating .txt files in the current directory from Slovak to English language. Please wait ...')
translate_files('sk', 'en')
