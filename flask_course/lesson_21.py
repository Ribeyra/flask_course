from flask import Flask, json, redirect, render_template, request   # noqa f401

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    # print(request.cookies)
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    return render_template('cart/index.html', cart=cart)


# BEGIN (write your solution here)
@app.post('/cart-items')
def cart_items_post():
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    data = request.form.to_dict()
    product_id = data['item_id']
    product = cart.setdefault(
        product_id, {'count': 0, 'name': data['item_name']}
    )
    product['count'] += 1

    answer = redirect('/', 302)
    answer.set_cookie('cart', json.dumps(cart))
    return answer


@app.post('/cart-items/clean')
def cart_items_clean_post():
    answer = redirect('/', 302)
    answer.delete_cookie("cart")
    return answer
# END
# json.dumps() и json.loads()
