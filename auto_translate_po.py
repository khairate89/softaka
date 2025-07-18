import polib
from deep_translator import GoogleTranslator
import os
import subprocess

# === CONFIGURATION ===
PO_FILE_PATH = 'locale/es/LC_MESSAGES/django.po'  # Adjust if needed
TARGET_LANG = 'es'

def auto_translate_po_file(po_path, lang):
    po = polib.pofile(po_path)
    translator = GoogleTranslator(source='auto', target=lang)

    for entry in po:
        if not entry.msgstr and entry.msgid and not entry.obsolete:
            try:
                translated = translator.translate(entry.msgid)
                entry.msgstr = translated
                print(f'Translated: "{entry.msgid}" -> "{translated}"')
            except Exception as e:
                print(f'Error translating "{entry.msgid}": {e}')

    po.save(po_path)
    print("\n✔️ Translation complete.")

    # Compile the messages (.mo file)
    compile_messages(po_path)

def compile_messages(po_path):
    # Go up to the project root (adjust if needed)
    project_root = os.path.abspath(os.path.join(os.path.dirname(po_path), '../../..'))
    print(f"Compiling messages from project root: {project_root}")

    env = os.environ.copy()
    env['DJANGO_SETTINGS_MODULE'] = 'filecr_clone_django_project.settings'  # Replace with your actual settings module

    try:
        subprocess.run(['django-admin', 'compilemessages'], cwd=project_root, env=env, check=True)
        print("✔️ Messages compiled.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Compile error: {e}")

if __name__ == "__main__":
    auto_translate_po_file(PO_FILE_PATH, TARGET_LANG)
