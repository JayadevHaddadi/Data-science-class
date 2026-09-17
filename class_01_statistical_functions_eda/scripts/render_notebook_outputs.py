import json
import io
import sys
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open('statistical_functions_eda_class_solutions.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Global execution namespace
glob_ns = {}

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source_code = "".join(cell['source'])
        
        # Capture stdout
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
            
            # Check if matplotlib created any figures
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

with open('statistical_functions_eda_class_solutions.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Successfully executed and pre-rendered all outputs in statistical_functions_eda_class_solutions.ipynb!")
