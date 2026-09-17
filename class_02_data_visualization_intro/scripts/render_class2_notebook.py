import json
import io
import sys
import os
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.chdir("class_02_data_visualization_intro")

with open('data_visualization_intro.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

glob_ns = {}

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source_code = "".join(cell['source'])
        
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        
        plt.close('all')
        
        try:
            exec(source_code, glob_ns)
            stdout_text = redirected_output.getvalue()
            
            outputs = []
            if stdout_text:
                outputs.append({
                    "name": "stdout",
                    "output_type": "stream",
                    "text": stdout_text.splitlines(keepends=True)
                })
            
            figs = [plt.figure(i) for i in plt.get_fignums()]
            for fig in figs:
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)
                img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                outputs.append({
                    "data": {
                        "image/png": img_base64,
                        "text/plain": ["<Figure size ...>"]
                    },
                    "metadata": {},
                    "output_type": "display_data"
                })
                plt.close(fig)
                
            cell['outputs'] = outputs
            cell['execution_count'] = 1
        except Exception as e:
            stdout_text = redirected_output.getvalue()
            cell['outputs'] = [{
                "ename": type(e).__name__,
                "evalue": str(e),
                "output_type": "error",
                "traceback": [str(e)]
            }]
            print(f"Error executing cell: {e}")
        finally:
            sys.stdout = old_stdout

with open('data_visualization_intro_solutions.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Pre-rendered data_visualization_intro_solutions.ipynb successfully!")
