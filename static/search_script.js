function searchColumn() {
  // Declare variables
  var inputs, filled_inputs, row_is_filtered, filters, table, tr, td, i, j, txtValue;
  filled_inputs=[];
  filters=[];
  inputs = document.getElementsByTagName("input");
  for (i=0;i<inputs.length;i++){
    if (inputs[i].value){
        filled_inputs.push(i);
        filters.push(inputs[i].value.toUpperCase());
        //console.log(inputs[i].value+" "+i);
    }
  }
  table = document.getElementById("main_table");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 1; i < tr.length; i++) {
  row_is_filtered=false;
    for (j = 0; j<filled_inputs.length; j++){
        td = tr[i].getElementsByTagName("td")[filled_inputs[j]];
        if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filters[j]) <= -1) {
            row_is_filtered=true;
            //console.log(txtValue+" "+filters[j]);
        }
    }
    }

    if(row_is_filtered){ tr[i].style.display = "none";}
    else{tr[i].style.display="";}
  }
}
