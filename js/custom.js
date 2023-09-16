let ga = document.getElementsByTagName("gradio-app");
let targetNode = ga[0];
let loaded = false;
let modify_title = false;
function gradioLoaded(mutations) {
    for (let i = 0; i < mutations.length; i++) {
        if (mutations[i].addedNodes.length) {
            keyboard_enter();
        }
    }

}

// 监视页面内部 DOM 变动
let observer = new MutationObserver(function (mutations) {
    gradioLoaded(mutations);
});
observer.observe(targetNode, { childList: true, subtree: true });


function keyboard_enter() {
    let submit_btn = document.querySelector('#submit-btn');
    let user_input = document.querySelector('#user-input textarea');
    if(submit_btn && user_input){
        if(submit_btn.getAttribute('data-listener') == null){
            submit_btn.setAttribute('data-listener', 'true');
            user_input.addEventListener('keydown', function (e) {
                if (e.ctrlKey && e.code === 'Enter') {
                    user_input.value += '\n';
                }else if (!e.ctrlKey && e.code === 'Enter') {
                    e.preventDefault();
                    if(user_input.value.trim().length == 0){
                        return;
                    }
                    submit_btn.click();
                }
            });
        }
    }
    let start_btn = document.querySelector('#start-btn');
    if(start_btn){
        if(start_btn.getAttribute('data-listener') == null){
            start_btn.setAttribute('data-listener', 'true');
            document.addEventListener('keydown', function (e) {
                if (e.shiftKey && e.code === 'KeyS') {
                    start_btn.click();
                }
            });
        }
    }
    let show_answer_btn = document.querySelector('#show-answer-btn');
    if(show_answer_btn){
        if(show_answer_btn.getAttribute('data-listener') == null){
            show_answer_btn.setAttribute('data-listener', 'true');
            document.addEventListener('keydown', function (e) {
                if (e.shiftKey && e.code === 'KeyN') {
                    show_answer_btn.click();
                }
            });
        }
    }
    let save_btn = document.querySelector('#save-btn');
    if(save_btn){
        if(save_btn.getAttribute('data-listener') == null){
            save_btn.setAttribute('data-listener', 'true');
            document.addEventListener('keydown', function (e) {
                if (e.shiftKey && e.code === 'KeyD') {
                    save_btn.click();
                }
            });
        }
    }
}
