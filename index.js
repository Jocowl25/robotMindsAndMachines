headers=document.querySelectorAll("header a")
headers.forEach(ele =>{
    if(ele.href==window.location.href){
        ele.style.fontWeight="bold"
    }
})