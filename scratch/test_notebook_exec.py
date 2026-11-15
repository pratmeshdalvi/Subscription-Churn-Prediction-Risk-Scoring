import json

with open('notebooks/01_data_validation.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

code_cells = [c['source'] for c in nb['cells'] if c['cell_type'] == 'code']
print(f"Total cells: {len(nb['cells'])}, Code cells: {len(code_cells)}")

full_code = '\n'.join(''.join(c) for c in code_cells)
clean_code = full_code.replace('plt.show()', '# plt.show()').replace('display(', 'print(')

exec(clean_code)
print('\n*** ALL AUDIT TESTS AND CODE EXECUTED PERFECTLY! ***')
