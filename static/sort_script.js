var COLUMN_MODE = []
var ORDER = []
prepare();
function prepare(){
    var i;
    for (i=0;i<document.getElementById("main_table").rows[0].cells.length;i++){
        COLUMN_MODE.push(0);
    }
}

function sortControl(column){
    var i;
    switch (COLUMN_MODE[column]){
        case 0:
            document.getElementById("main_table").rows[0].cells[column].style.background="Green";
            COLUMN_MODE[column]=1;
            ORDER.push(column);
            sort()
        break;
        case 1:
            document.getElementById("main_table").rows[0].cells[column].style.background="Red";
            COLUMN_MODE[column]=2;
            sort()

        break;
        case 2:
            document.getElementById("main_table").rows[0].cells[column].style.background="White";
            COLUMN_MODE[column]=0;
            if(ORDER.indexOf(column)>-1){
                ORDER.splice(ORDER.indexOf(column),1)
            }
            if (ORDER.length>0){sort()}

        break;
    }
}

function sort(){
    var i, table, arr, newTbody, isColumnFloat,rows;

    arr = [];
    rows=document.getElementsByTagName("tr");
    isColumnFloat=true;
    for (i=1;i<rows.length;i++){
        arr.push(rows[i]);
        if (!parseFloat(rows[i].getElementsByTagName('td')[ORDER[ORDER.length-1]].textContent)){
            isColumnFloat=false;
        }
    }
    if (isColumnFloat){
        //arr=bubbleSort(arr,column,ascending);
        //arr=quickSortFloat(arr,column,ascending);
        //console.log(arr);
        //console.log(ORDER);
        //console.log(COLUMN_MODE);
        arr = recSort(arr,ORDER[0],0,(COLUMN_MODE[ORDER[0]]==1));
    }
    else{
        //arr=bubbleSort(arr,column,ascending);
        //arr=quickSort(arr,column,ascending);
        //console.log(arr);
        //console.log(ORDER);
        //console.log(COLUMN_MODE);
        arr = recSort(arr,ORDER[0],0,(COLUMN_MODE[ORDER[0]]==1));
    }
    //console.log(arr);
    newTbody = document.createElement('tbody')
    for (i=0;i<arr.length;i++){
        newTbody.appendChild(arr[i]);
        //console.log(arr[i]);
    }
    table = document.getElementById("main_table");
    table.replaceChild(newTbody,table.getElementsByTagName("tbody")[0])
}
function quickSortFloat(arr,column,ascend) {
  if (arr.length < 2) return arr;
  var pivot = arr[0];
  const left = [];
  const right = [];
  for (var i = 1; i < arr.length; i++) {

    if (parseFloat(pivot.getElementsByTagName("td")[column].textContent) > parseFloat(arr[i].getElementsByTagName("td")[column].textContent)) {
      if(ascend){left.push(arr[i]);}
      else{right.push(arr[i])}
    } else {
      if(ascend){right.push(arr[i]);}
      else{left.push(arr[i]);}
    }
  }
  return quickSortFloat(left,column,ascend).concat(pivot, quickSortFloat(right,column,ascend));
}

function quickSort(arr,column,ascend) {
  if (arr.length < 2) return arr;
  let pivot = arr[0];
  const left = [];
  const right = [];
  for (let i = 1; i < arr.length; i++) {
    if (pivot.getElementsByTagName("td")[column].textContent > arr[i].getElementsByTagName("td")[column].textContent) {
      if(ascend){left.push(arr[i]);}
      else{right.push(arr[i])}
    } else {
      if(ascend){right.push(arr[i]);}
      else{left.push(arr[i]);}
    }
  }
  return quickSort(left,column,ascend).concat(pivot, quickSort(right,column,ascend));
}

function getContent(row,column){
    return row.getElementsByTagName("td")[column].textContent
}

function recSort(arr,column,orderIndex,asc){
    if(orderIndex>=ORDER.length){
        return arr;
    }
    /*
    console.log("recSort:\n")
    console.log(arr)
    console.log(ORDER)
    console.log(COLUMN_MODE)
    console.log("\ncolumn: "+column+"\norderIndex: "+orderIndex+"\nasc: "+asc)
    */
    rows=document.getElementsByTagName("tr");
    var isColumnFloat=true;
    for (i=1;i<rows.length;i++){
        if (!parseFloat(rows[i].getElementsByTagName('td')[ORDER[ORDER.length-1]].textContent)){
            isColumnFloat=false;
        }
    }
    if(isColumnFloat){
        arr=quickSortFloat(arr,column,asc);
    }
    else{
        arr=quickSort(arr,column,asc);
    }
    var i,j,eqArr;
    for(i = 0;i<arr.length-1;i++){
        eqArr=[];
        if(getContent(arr[i],column)===(getContent(arr[i+1],column))){
            eqArr.push(arr[i])
            for (j = 0; (i+j+1<arr.length)&&(getContent(arr[i],column)===(getContent(arr[i+j+1],column)));j++){
                eqArr.push(arr[i+j+1])
            }
            console.log(eqArr);
            eqArr=recSort(eqArr,ORDER[orderIndex+1],orderIndex+1,(COLUMN_MODE[ORDER[orderIndex+1]]==1))
            console.log(eqArr);
            console.log(ORDER);
            console.log(orderIndex);
            for (j = 0; j<eqArr.length;j++){
                arr[i+j]=eqArr[j];
            }
            i+=j-1;

        }
    }
    return arr;
}