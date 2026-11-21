import zipfile
import json

z = zipfile.ZipFile('churn.pbix', 'r')
pages_data = json.loads(z.read('Report/definition/pages/pages.json').decode('utf-8'))
print('Active page:', pages_data.get('activePageName'))

for p in pages_data.get('pageOrder', []):
    p_info = json.loads(z.read(f'Report/definition/pages/{p}/page.json').decode('utf-8'))
    print(f"\nPage: {p_info.get('displayName')} (ID: {p})")
    v_files = [f for f in z.namelist() if f.startswith(f'Report/definition/pages/{p}/visuals/')]
    for vf in v_files:
        try:
            v_info = json.loads(z.read(vf).decode('utf-8'))
            vis = v_info.get('visual', {})
            v_type = vis.get('visualType')
            pos = v_info.get('position', {})
            print(f"  Visual: {v_type} | X:{pos.get('x')} Y:{pos.get('y')} W:{pos.get('width')} H:{pos.get('height')}")
        except Exception as e:
            pass
