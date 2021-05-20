document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#pdf-upload").onchange = function(){
        document.querySelector("#file-name").textContent = this.files[0].name;
    }
});