function showVal(x){
    x = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    document.getElementById('sel_price').innerText = x;
}

function removeURLParameter(url, parameter) {
    var urlParts = url.split('?');
    if (urlParts.length < 2) {
        return url; // پارامتری وجود نداره
    }

    var prefix = encodeURIComponent(parameter) + '=';
    var params = urlParts[1].split('&');

    // حذف همه‌ی پارامترهایی که با کلید داده شده شروع می‌شن
    params = params.filter(function(param) {
        return param.lastIndexOf(prefix, 0) !== 0;
    });

    return urlParts[0] + (params.length > 0 ? '?' + params.join('&') : '');
}


function select_sort(){
    var select_sort_value = $("#select_sort").val();
    var url = removeURLParameter(window.location.href, 'sort_type');
    var separator = url.indexOf('?') === -1 ? '?' : '&';
    window.location = url + separator + "sort_type=" + select_sort_value;
}

function select_show_count() {
    var select_show_value = $("#select_show_count").val();
    var url = removeURLParameter(window.location.href, 'show_count');
    var separator = url.includes("?") ? "&" : "?";
    window.location = url + separator + "show_count=" + select_show_value;
}

function reset_filters() {
    // URL فعلی
    var url = new URL(window.location.href);
    // لیست پارامترهایی که میخوای نگه داری
    var keepParams = ['page', 'show_count'];

    // حذف همه پارامترها به جز keepParams
    url.searchParams.forEach((value, key) => {
        if (!keepParams.includes(key)) {
            url.searchParams.delete(key);
        }
    });

    // ری‌دایرکت به URL جدید
    window.location = url.toString();
}

// ----- shop cart -----
status_shop_cart();

function status_shop_cart(){
    $.ajax({
        type: 'GET',
        url: '/orders/status_shop_cart/',
        success: function(res){
            // alert('کالای مورد نظر به سبد خرید شما اضافه شد');
            $('#indicator__value').text(res);
        }
    })
}

function add_to_shop_cart(product_id,qty){
    if(qty===0){
        qty=$('#product-quantity').val();
    }
    $.ajax({
        type: 'GET',
        url: '/orders/add_to_shop_cart/',
        data: {
            product_id:product_id,
            qty:qty,
        },
        success: function(res){
            // alert('کالای مورد نظر به سبد خرید شما اضافه شد');
            status_shop_cart();

        }
    })
}

function delete_from_shop_cart(product_id){
    $.ajax({
        type: 'GET',
        url: '/orders/delete_from_shop_cart/',
        data: {
            product_id:product_id,
        },
        success: function(res){
            // alert("کالای مورد نظر از سبد خرید شما حذف شد");
            $('#shop_cart_list').html(res);
            status_shop_cart();
        }
    })
    
}

function update_shop_cart(){
    var product_id_list=[]
    var qty_list=[]
    $("input[id^='qty_']").each(function(index){
        product_id_list.push($(this).attr("id").slice(4));
        qty_list.push($(this).val())
    })

    $.ajax({
        type: 'GET',
        url: '/orders/update_shop_cart/',
        data: {
            product_id_list:product_id_list,
            qty_list:qty_list,
        },
        success: function(res){
            // alert("کالای مورد نظر از سبد خرید شما حذف شد");
            $('#shop_cart_list').html(res);
            status_shop_cart();
        }
    })
    
}



function showCreateComment(productId, commentId, slug) {
    $.ajax({
        type: 'GET',
        url: '/csf/create_comment/' + slug,
        data: {
            productId: productId,
            commentId: commentId,
        },
        success: function(res) {
            // مخفی کردن دکمه پاسخ
            $('#btn_' + commentId).hide();

            // فرم partial را مستقیماً در div قرار می‌دهیم
            $('#comment_form_' + commentId).html(res);

            // اضافه کردن ضربدر روی div comment_form
            const closeBtn = $(`
                <button type="button" 
                        class="btn btn-sm btn-danger" 
                        style="position: absolute; top: 5px; right: 5px; z-index: 10;">
                    ✖
                </button>
            `);

            // اضافه کردن padding-top کافی برای فرم تا ضربدر روی متن نیفتد
            $('#comment_form_' + commentId).css({
                'position': 'relative',
                'padding-top': '35px'
            }).prepend(closeBtn);

            // کلیک روی ضربدر فرم را مخفی کند و دکمه پاسخ دوباره نمایش داده شود
            closeBtn.on('click', function() {
                closeCreateComment(commentId);
            });
        }
    });
}

function closeCreateComment(commentId) {
    $('#comment_form_' + commentId).html('');
    $('#btn_' + commentId).show();
}


function addScore(score, productId) {
    var starRatings = document.querySelectorAll(".fa-star");

    // همه ستاره‌ها رو خالی کنیم
    starRatings.forEach(element => {
        element.classList.remove("checked");
    });

    // ستاره‌های انتخاب شده رو پر کنیم
    for (let i = 1; i <= score; i++) {
        const element = document.getElementById("start_" + i);
        if (element) {
            element.classList.add("checked");
        }
    }

    // ارسال امتیاز به سرور
    $.ajax({
        type: 'GET',
        url: '/csf/add_score/',
        data: {
            productId: productId,
            score: score,
        },
        success: function(res) {
            // console.log("امتیاز ثبت شد:", res);

            // فرض می‌کنیم سرور میانگین جدید رو توی res.average_score برگردونه
            if (res.average_score) {
                document.getElementById("average-score").innerText = res.average_score;
            }
        }
    });

    // بعد از کلیک، همه ستاره‌ها disable بشن
    starRatings.forEach(element => {
        element.classList.add("disable");
    });
}

function status_favorites(){
    $.ajax({
        type: 'GET',
        url: '/csf/status_favorites/', // ← مطمئن شو با urls.py مطابقت دارد
        success: function(res){
            $('.indicator__value2').text(res);
        },
        error: function(xhr){
            console.log("خطا در دریافت تعداد علاقه‌مندی‌ها:", xhr.responseText);
        }
    });
}


function addToFavorites(productId){
    $.ajax({
        type: 'GET',
        url: '/csf/add_to_favorites/',
        data: { product_id: productId },
        success: function(res){
            if(res.status === 'ok'){
                $('#favorite-btn-' + productId).addClass('btn-icon1');
                status_favorites(); // عدد بروزرسانی می‌شود
            }
        }
    });
}

// هنگام بارگذاری صفحه
$(document).ready(function(){
    status_favorites();
});


status_of_compare_list()
function status_of_compare_list(){
    $.ajax({
        type: 'GET',
        url: '/products/status_of_compare_list/',
        success: function(res){
            if (Number(res) === 0){
                $('#compare_count_icon').hide();
            }
            else{
                $('#compare_count_icon').show();
                $('#compare_count').text(res);
            }
        }
    })
}


function addToCompareList(productId,productGroupId) {
    $.ajax({
        type: 'GET',
        url: "/products/add_to_compare_list/",
        data: {
            productId:productId,
            productGroupId:productGroupId,
        },
        success: function(res){
            alert(res);
            status_of_compare_list()
        }
    })
}

function deleteFromCompareList(productId){
    $.ajax({
        type: 'GET',
        url: '/products/delete_from_compare_list/',
        data: {
            productId:productId,
        },
        success: function(res){
            $('#compare_list').html(res);
            status_of_compare_list();
        }
    })
}