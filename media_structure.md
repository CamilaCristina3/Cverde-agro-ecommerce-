Media directory structure (created locally):

media/
├── categories/
│   ├── frutas/
│   │   ├── laranja.svg
│   │   ├── tangerina.svg
│   │   └── limao.svg
│   ├── legumes/
│   │   ├── alface.svg
│   │   ├── cenoura.svg
│   │   └── abobora.svg
│   └── default-category.svg
│
├── products/
│   ├── abacate.svg
│   ├── alface.svg
│   ├── abobora.svg
│   └── product_placeholder.svg
│
└── producers/
    └── placeholder_producer.svg

Notes:
- Each category has: `nome`, `descricao`, and an `icone`/`imagem` entry in `media/categories/categories.json`.
- The file `media/categories/categories.json` lists the demo categories and image paths.

Git / tracking note:
- This project currently ignores the `media/` folder via `.gitignore` to avoid committing user uploads and large binaries.
- The files created under `media/` in this workspace are local and will NOT be pushed while `media/` is excluded by `.gitignore`.
- To include these media files in the repository (not recommended for large/production files), remove or update the `media/` line in `.gitignore`, then add and commit the files.

If you want, I can:
- (A) Remove `media/` from `.gitignore` and commit the created placeholders (useful for submission).
- (B) Move these placeholder images to `static/images/` so they are tracked and served from static assets (recommended for demo placeholders).

Which option do you prefer?