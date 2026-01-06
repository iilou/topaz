import os
from pypdf import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_OFFLINE"] = "0" # Ensure it can still download


def split_and_convert(input_pdf, output_md, batch_size=50):
    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)
    
    # 1. Setup Docling with Low-RAM settings
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_table_structure = True  # Keep tables
    pipeline_options.do_ocr = True             # For images/scans
    
    # Use PyPdfium backend (Fastest and most memory-efficient for 8GB RAM)
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend 
            )
        }
    )

    with open(output_md, "a", encoding="utf-8") as final_file:
        for start in range(0, total_pages, batch_size):
            end = min(start + batch_size, total_pages)
            print(f"Processing pages {start} to {end}...")

            # 2. Create a temporary small PDF for this batch
            writer = PdfWriter()
            for i in range(start, end):
                writer.add_page(reader.pages[i])
            
            temp_pdf = f"temp_batch_{start}.pdf"
            with open(temp_pdf, "wb") as f:
                writer.write(f)

            # 3. Convert the small batch
            result = converter.convert(temp_pdf)
            final_file.write(result.document.export_to_markdown())
            final_file.write("\n\n") # Add spacing between batches

            # 4. CRITICAL: Clear RAM
            # result.input._backend.unload()  # Manual memory release
            os.remove(temp_pdf) # Delete temp file
            
    print(f"Done! 3,000 pages converted to {output_md}")

# Run it
split_and_convert("genetics_textbook.pdf", "genetics_full.md")