const filterForm = document.getElementById("formFiltros");
const selectedDate = document.getElementById("dataFiltro");
const selectedMonth = document.getElementById("mes");

if (filterForm && selectedDate && selectedMonth) {
    function updateSelectedMonth() {
        selectedMonth.value = selectedDate.value ? selectedDate.value.slice(0, 7) : "";
    }

    selectedDate.addEventListener("change", updateSelectedMonth);
    filterForm.addEventListener("submit", updateSelectedMonth);
}
