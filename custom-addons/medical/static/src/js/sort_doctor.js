/* @odoo-module */

import { jsonrpc } from "@web/core/network/rpc_service";

let sortBtns = document.querySelectorAll('.sort-by-options__option')
if (sortBtns) {
    sortBtns.forEach(item => {
        item.addEventListener('click', (e) => {
            let sortBtns = document.querySelectorAll('.sort-by-options__option')
            if (sortBtns) {
                sortBtns.forEach(item => {
                    if (item.classList.contains('sort-by-options__option--selected')) {
                        if (item.classList.contains('sort-by-price')) {
                            let sortPriceBtn = document.querySelector('.sort-price-select')
                            sortPriceBtn.classList.remove('active')
                            sortPriceBtn.innerHTML = "Gía khám"
                        }
                        item.classList.remove('sort-by-options__option--selected')
                    }
                })
            }
            e.target.classList.add('sort-by-options__option--selected')
        })
    })
}

$(document).ready(function () {
    let sortPriceBtn = document.querySelector('.sort-price-select')
    let sortPriceOptions = document.querySelectorAll('.sort-by-price')
    if (sortPriceOptions) {
        sortPriceOptions.forEach(item => {
            item.addEventListener('click', async (e) => {
                sortPriceBtn.innerHTML = e.target.textContent
                sortPriceBtn.classList.add('active')
                let type = 'desc'
                if (e.target.getAttribute("data-ordertype")) {
                    type = e.target.getAttribute("data-ordertype")
                }

                let currentUrl = new URL(window.location.href);
                let params = new URLSearchParams(currentUrl.search);
                params.set('sort', 'price');
                params.set('order', type);
                currentUrl.search = params.toString();
                window.history.pushState({}, '', currentUrl.toString());

                await jsonrpc('/sort_doctor', {
                    'sort': 'price',
                    'order': type
                })
                    .then(function (result) {
                        // console.log(result)
                        $(`#doctor_list`).html(result)
                    })
                    .catch(function (error) {
                        console.error('Error:', error);
                    })
            })
        })
    }

    let sortBtns = document.querySelectorAll('.sort-by-options__option')
    if (sortBtns) {
        sortBtns.forEach(item => {
            item.addEventListener('click', async (e) => {
                if (!item.classList.contains('sort-by-price')) {
                    let sort = 'default'
                    if (e.target.getAttribute("data-ordertype")) {
                        sort = e.target.getAttribute("data-ordertype")
                    }

                    let currentUrl = new URL(window.location.href);
                    let params = new URLSearchParams(currentUrl.search);
                    params.set('sort', sort);
                    params.delete('order');
                    currentUrl.search = params.toString();
                    window.history.pushState({}, '', currentUrl.toString());

                    await jsonrpc('/sort_doctor', {
                        'sort': sort,
                    })
                        .then(function (result) {
                            // console.log(result)
                            $(`#doctor_list`).html(result)
                        })
                        .catch(function (error) {
                            console.error('Error:', error);
                        })
                }
            })
        })
    }
})