const expressionInput = document.getElementById("expression");
const treeButton = document.getElementById("tree");
const buttons = document.querySelectorAll(".buttons button");

let expression = "";

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    const buttonText = button.textContent;

    if (buttonText === "C") {
      expression = "";
    } else if (buttonText === "=") {
      expression = evaluate(expression); 
    } else if (buttonText == "Tree") {
      console.log("Generando arbol");
    } else {
      expression += buttonText;
    }
    expressionInput.value = expression;
  });
});

function evaluate(expression) {
  try {
    return eval(expression);
  } catch (e) {
    return "Error";
  }
}

document.getElementById("dot").addEventListener("click", () => {
  const display = document.getElementById("display");
  const currentValue = display.value;

  if (!currentValue.includes(".")) {
    display.value += ".";
  }
});

treeButton.addEventListener("click", async () => {
  const expression = expressionInput.value;

  const response = await fetch("/generate_tree", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression }),
  });
console.log(response);

  const data = await response.json();
  const treeImage = data.tree_image;
  console.log(treeImage);
  console.log(data.tree_image);

  const treeContainer = document.getElementById("tree-container");
  treeContainer.innerHTML = `<img src="/static/${treeImage}" alt="Árbol Binario" />`;
});
