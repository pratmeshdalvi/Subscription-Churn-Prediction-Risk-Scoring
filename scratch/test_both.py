import json
from pathlib import Path

for nb_file in ['notebooks/01_data_validation.ipynb', 'notebooks/02_eda.ipynb']:
    with open(nb_file, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    code_cells = [c['source'] for c in nb['cells'] if c['cell_type'] == 'code']
    full_code = '\n'.join(code_cells)
    clean_code = full_code.replace('plt.show()', '# plt.show()').replace('display(', 'print(')

    try:
        exec(clean_code)
        print(f'\n✅ {nb_file} — PASSED')
    except Exception as e:
        print(f'\n❌ {nb_file} — FAILED: {e}')
