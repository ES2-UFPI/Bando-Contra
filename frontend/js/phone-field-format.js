function phoneMask() {
  var num = $(this).val().replace(/\D/g,'');
  var char_cel = {0: '(', 2:')', 7: '-'}
  var char_tel = {0: '(', 2:')', 6: '-'}
  var value = '';
  for(var i = 0; i < num.length; i++){
    if(num.length < 11)
      value += (char_tel[i]||'') + num[i]
    else if(i < 11)
      value += (char_cel[i]||'') + num[i]
  }
  $(this).val(value)
}
$('[type="tel"]').keyup(phoneMask);