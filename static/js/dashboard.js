let dashboardButtonA = document.getElementById(elementId='dashboard-button-a')
let dashboardButtonB = document.getElementById(elementId='dashboard-button-b')
let dashboardButtonC = document.getElementById(elementId='dashboard-button-c')
let dashboardContainerA = document.getElementById(elementId='nav-profile-box-a')
let dashboardContainerB = document.getElementById(elementId='nav-profile-box-b')
let dashboardContainerC = document.getElementById(elementId='nav-profile-box-c')
let dashboardStyleContainerA = document.getElementById(elementId='dashboard-nav-button-a')
let dashboardStyleContainerB = document.getElementById(elementId='dashboard-nav-button-b')
let dashboardStyleContainerC = document.getElementById(elementId='dashboard-nav-button-c')

dashboardButtonA.addEventListener(type='click', listener=() => {
    dashboardContainerA.style.display = 'block'
    dashboardStyleContainerA.classList.add('js-button-highlight-on')
    dashboardStyleContainerA.classList.remove('js-button-highlight-off')
    dashboardContainerB.style.display = 'none'
    dashboardStyleContainerB.classList.add('js-button-highlight-off')
    dashboardStyleContainerB.classList.remove('js-button-highlight-on')
    dashboardContainerC.style.display = 'none'
    dashboardStyleContainerC.classList.add('js-button-highlight-off')
    dashboardStyleContainerC.classList.remove('js-button-highlight-on')
})

dashboardButtonB.addEventListener(type='click', listener=() => {
    dashboardContainerA.style.display = 'none'
    dashboardStyleContainerA.classList.add('js-button-highlight-off')
    dashboardStyleContainerA.classList.remove('js-button-highlight-on')
    dashboardContainerB.style.display = 'block'
    dashboardStyleContainerB.classList.add('js-button-highlight-on')
    dashboardStyleContainerB.classList.remove('js-button-highlight-off')
    dashboardContainerC.style.display = 'none'
    dashboardStyleContainerC.classList.add('js-button-highlight-off')
    dashboardStyleContainerC.classList.remove('js-button-highlight-on')
})

dashboardButtonC.addEventListener(type='click', listener=() => {
    dashboardContainerA.style.display = 'none'
    dashboardStyleContainerA.classList.add('js-button-highlight-off')
    dashboardStyleContainerA.classList.remove('js-button-highlight-on')
    dashboardContainerB.style.display = 'none'
    dashboardStyleContainerB.classList.add('js-button-highlight-off')
    dashboardStyleContainerB.classList.remove('js-button-highlight-on')
    dashboardContainerC.style.display = 'block'
    dashboardStyleContainerC.classList.add('js-button-highlight-on')
    dashboardStyleContainerC.classList.remove('js-button-highlight-off')
})

dashboardButtonD.addEventListener(type='click', listener=() => {
    dashboardContainerA.style.display = 'none'
    dashboardStyleContainerA.classList.add('js-button-highlight-off')
    dashboardStyleContainerA.classList.remove('js-button-highlight-on')
    dashboardContainerB.style.display = 'none'
    dashboardStyleContainerB.classList.add('js-button-highlight-off')
    dashboardStyleContainerB.classList.remove('js-button-highlight-on')
    dashboardContainerC.style.display = 'none'
    dashboardStyleContainerC.classList.add('js-button-highlight-off')
    dashboardStyleContainerC.classList.remove('js-button-highlight-on')
})