function groups_selectAllWords(theList) {
  myList = document.getElementById(theList);
  for (var x=0; x < myList.length; x++) {
    myList[x].selected="selected";
  }
}

function groups_addNewKeyword(toList, newText, newValue) {
  theToList=document.getElementById(toList);
  for (var x=0; x < theToList.length; x++) {
    if (theToList[x].text == newText) {
      return false;
    }
  }
  theLength = theToList.length;
  theToList[theLength] = new Option(newText);
  theToList[theLength].value = newValue;
}

function groups_moveKeywords(fromList,toList,selectThese, forSubmit) {
  theFromList=document.getElementById(fromList);
  for (var x=0; x < theFromList.length; x++) {
    if (theFromList[x].selected) {
      groups_addNewKeyword(toList, theFromList[x].text, theFromList[x].value);
    }
  }
  theToList=document.getElementById(fromList);
  for (var x=theToList.length-1; x >= 0 ; x--) {
    if (theToList[x].selected) {
      theToList[x] = null;
    }
  }
  groups_selectAllWords(selectThese);
  copyDataForSubmit(forSubmit);
}

// copy each item of "toSel" into one hidden input field
function copyDataForSubmit(name)
{
  // shortcuts for selection field and hidden data field
  var toSel = document.getElementById(name);
  var toDataContainer = document.getElementById(name+"-toDataContainer");

  // delete all child nodes (--> complete content) of "toDataContainer" span
  while (toDataContainer.hasChildNodes())
      toDataContainer.removeChild(toDataContainer.firstChild);

  // create new hidden input fields - one for each selection item of
  // "to" selection
  for (var i = 0; i < toSel.options.length; i++)
  {
    // create virtual node with suitable attributes
    var newNode = document.createElement("input");
    var newAttr = document.createAttribute("name");
    name = name.replace('_to','');
    newAttr.nodeValue = name.replace(/-/g, '.')+':list';
    newNode.setAttributeNode(newAttr);

    newAttr = document.createAttribute("type");
    newAttr.nodeValue = "hidden";
    newNode.setAttributeNode(newAttr);

    newAttr = document.createAttribute("value");
    newAttr.nodeValue = toSel.options[i].value;
    newNode.setAttributeNode(newAttr);

    // actually append virtual node to DOM tree
    toDataContainer.appendChild(newNode);
  }
}