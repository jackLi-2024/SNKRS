#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from selenium import webdriver


def get_cookie():
    result = ""
    browser = webdriver.Firefox()
    browser.get(url="https://www.qichacha.com/")
    cookies = browser.get_cookies()
    for one in cookies:
        k = one.get("name", "")
        v = one.get("value", "")
        s = k + "=" + v + ";"
        result += s
    print result


import execjs


def get_tot(tk="a4lf9K", bid="287832028393"):
    """https://xin.baidu.com/detail/changeajax?
    pid=5-F6k0n5hFNkIjttQ*iujb7bC7hArRa7CwCL&
    p=1
    &tot=9gL2Vd6KlncoVdbw-opN-cyD2A0IXUrz9QPi
    &_=1533698401505"""
    # 参数中pid可以直接获得
    # tot无法直接获得，需要破解
    js_func = """
            function mix(tk, bid) {
                tk = tk.split('');
                var bdLen = bid.length;
                bid = bid.split('');
                for(var i = bdLen - 1; i >= 0; i -= 2) {
                    var tmp = tk[bid[i]];
                    tk[bid[i]] = tk[bid[i - 1]];
                    tk[bid[i - 1]] = tmp;
                    }
                return tk.join("");
                }
    """
    # (function(){
    #                     var tk = document.getElementById('tIwe3i7').getAttribute('a4lf9K');
    #                     var baiducode = document.getElementById('baiducode').innerText;
    #                     window.tk = mix(tk, baiducode);})();
    # 这是直接截取的js函数的代码，可知window.tk调用mix()函数,需要tk（页面中的标签），baiducode（页面的百度代码）两个参数
    ctx = execjs.compile(js_func)
    print ctx.call("mix", tk, bid)


if __name__ == '__main__':
    get_tot()
