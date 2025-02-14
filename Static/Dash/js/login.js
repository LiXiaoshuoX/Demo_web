function submitForm() {
    let formData = new FormData(document.getElementById('login-form'));
    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'login/', true);
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            if (response.success) {
                // 登录成功，获取next参数并跳转到相应的页面
                let next = String(formData.get('next'));
                if (next) {
                    window.location.href = next;
                } else {
                    window.location.href = 'index/';
                }
                } else {
                    // 登录失败，显示错误信息
                    alert(response.message);
                }
            }
        };
        xhr.send(formData);
    }
    //
    // document.getElementById('captcha-image').addEventListener('click', function() {
    //     // 发送 AJAX 请求来获取新的验证码
    //     let xhr = new XMLHttpRequest();
    //     xhr.open('GET', '/start/refresh_captcha/', true);
    //     xhr.onreadystatechange = function() {
    //         if (xhr.readyState === 4 && xhr.status === 200) {
    //             let data = JSON.parse(xhr.responseText);
    //             document.getElementById('captcha-image').src = data.captcha_image_url;
    //             document.getElementById('captcha_0').value = data.captcha_key;
    //         }
    //     };
    //     xhr.send();
    // });