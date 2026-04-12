// JavaScript para tornar o formulário de avaliação dinâmico
// Mostra/esconde campos Produto e Produtor conforme o tipo de avaliação

document.addEventListener("DOMContentLoaded", function () {
  const reviewTypeField = document.querySelector("#id_review_type");
  const productRow =
    document.querySelector(".form-row.field-product") ||
    document.querySelector(".field-product");
  const producerRow =
    document.querySelector(".form-row.field-producer") ||
    document.querySelector(".field-producer");

  function setVisible(element, visible) {
    if (!element) return;
    element.style.display = visible ? "" : "none";
  }

  function setRequired(selector, required) {
    const el = document.querySelector(selector);
    if (el) el.required = required;
  }

  function toggleFields() {
    if (!reviewTypeField) return;

    const selectedType = reviewTypeField.value;

    if (selectedType === "product") {
      setVisible(productRow, true);
      setVisible(producerRow, false);
      setRequired("#id_product", true);
      setRequired("#id_producer", false);
    } else if (selectedType === "producer") {
      setVisible(productRow, false);
      setVisible(producerRow, true);
      setRequired("#id_product", false);
      setRequired("#id_producer", true);
    } else {
      // Sem seleção: mostrar ambos para evitar bloquear o utilizador
      setVisible(productRow, true);
      setVisible(producerRow, true);
      setRequired("#id_product", false);
      setRequired("#id_producer", false);
    }
  }

  toggleFields();
  if (reviewTypeField) {
    reviewTypeField.addEventListener("change", toggleFields);
  }
});

