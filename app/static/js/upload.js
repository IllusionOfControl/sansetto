function _(el) {
    return document.getElementById(el);
}

function submitImagesUploadForm(event) {
    let images = _("imageFilesInput").files;
    let action = _("images-upload-form").getAttribute("action")

    let formData = new FormData();
    for (let i = 0; i < images.length; i++) {
        formData.append("images[]", images[i]);
    }
    let ajax = new XMLHttpRequest();
    ajax.upload.addEventListener("progress", progressHandler, false);
    ajax.addEventListener("load", completeHandler, false);
    ajax.addEventListener("error", errorHandler, false);
    ajax.addEventListener("abort", abortHandler, false);
    ajax.addEventListener("readystatechange", stateChangeHandler, false);
    ajax.addEventListener("loadstart", uploadStartHandler, false);
    ajax.open("POST", action);
    ajax.send(formData);

    event.preventDefault();
}

function progressHandler(event) {
    const percent = Math.round((event.loaded / event.total) * 100);

    let uploadStatus = _("upload-status");
    uploadStatus.innerHTML = `Uploaded ${event.loaded / 1024} kilobytes of ${event.total / 1024}`;

    let uploadProgressBar = _("upload-progress-bar");
    uploadProgressBar.style.width = `${percent}%`;
    uploadProgressBar.setAttribute("aria-valuenow", percent.toString());
}

function uploadStartHandler(event) {
    let uploadInfo = _("upload-info");
    uploadInfo.style.visibility = "visible";
}

function stateChangeHandler(event) {
    if (this.readyState === XMLHttpRequest.DONE) {
        // window.location.href = this.responseURL;
    }
}

function completeHandler(event) {
    _("upload-status").innerHTML = "Upload Success";
}

function errorHandler(event) {
    window.location.href = event.redirect;
    _("upload-status").innerHTML = "Upload Failed";
}

function abortHandler(event) {
    _("upload-status").innerHTML = "Upload Aborted";
}

imagesUploadForm = _("images-upload-form")
imagesUploadForm.addEventListener("submit", submitImagesUploadForm)