import subprocess
import tempfile
import os

def compile_latex_to_pdf(latex_code: str) -> bytes | None:
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file_path = os.path.join(temp_dir, "cv.tex")
            pdf_file_path = os.path.join(temp_dir, "cv.pdf")
            
            with open(tex_file_path, "w") as f:
                f.write(latex_code)
                
            # Run pdflatex twice to resolve references if any (standard practice)
            # -interaction=nonstopmode prevents hanging on errors
            # -output-directory ensures output goes to temp_dir
            cmd = ["pdflatex", "-interaction=nonstopmode", "-output-directory", temp_dir, tex_file_path]
            
            # First pass
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"LaTeX compilation error (stdout): {result.stdout}")
                print(f"LaTeX compilation error (stderr): {result.stderr}")
                return None
            
            # Read the generated PDF
            if os.path.exists(pdf_file_path):
                with open(pdf_file_path, "rb") as f:
                    return f.read()
                    
    except subprocess.CalledProcessError as e:
        print(f"LaTeX compilation failed: {e.stderr.decode()}")
    except Exception as e:
        print(f"Error during PDF generation: {e}")
            
    return None
