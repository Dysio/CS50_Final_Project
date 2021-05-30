document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#pdf-upload").onchange = function(){
        document.querySelector("#file-name").textContent = this.files[0].name;
    }

});

function showDiv() {
    document.getElementId("download-link").style.display = "block";
}