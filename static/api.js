$('form').on( 'submit', async function () {
    const flavor = $('#flavor').val();
    const rating = $('#rating').val();
    const size = $('#size').val();
    const img = $('#img').val();
    console.log(flavor, rating, size, img)
    await axios.post('/api/cupcakes', {
        flavor,
        rating,
        size,
        img
    })
});
