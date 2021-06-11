addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('.btn_menu')
    if(btn){
        btn.addEventListener('click', () => {
            const items = document.querySelector('.menu_item')
            items.classList.toggle('show')
        })
    }
})