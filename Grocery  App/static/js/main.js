function check_me(input_id) {
    var checkbox_input = document.querySelector('input[value="' + input_id + '"]');
    var checkbox_label = document.querySelector('label[for="' + input_id + '"]');

    if (checkbox_input && checkbox_label) {
        if (checkbox_input.checked) {
            checkbox_label.style.textDecoration = "line-through";
        } else {
            checkbox_label.style.textDecoration = "none";
        }
    }

    var btn = document.getElementById("remove_btn");
    if (btn) {
        btn.value = "Remove Items";
        btn.style.color = "#FFFFFF";
        btn.style.backgroundColor = "#FE7575";
        btn.style.cursor = "pointer";
    }
}

