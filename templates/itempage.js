window.addEventListener('load', () => {

    const params = (new URL(document.location)).searchParams;
    const item_name = params.get('item_name');
    const item_price = params.get('price');
    const item_description = params.get('item_description');
    const photo = params.get('photo');
    const name = params.get('userName');
    const email = params.get('email');
    const phoneNumber = params.get('phoneNumber');

    document.getElementById('item_name').innerHTML = item_name;
    document.getElementById('item_price').innerHTML = item_price;
    document.getElementById('item_description').innerHTML = item_description;
    document.getElementById('photo').innerHTML = photo;
    document.getElementById('userName').innerHTML = name;
    document.getElementById('email').innerHTML = email;
    document.getElementById('phoneNumber').innerHTML = phoneNumber;
}
