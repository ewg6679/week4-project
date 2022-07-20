function setUserInfo(){
    if(typeof(Storage)!=="undefined")
    {
    localStorage.userName = document.getElementById("")
    }
    else
    {
    document.getElementById("notes").innerHTML="Sorry, your browser does not support web storage...";
    }
}
