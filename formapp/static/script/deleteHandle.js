let del = (e, formid) => {

    event.preventDefault()

    let con = confirm('Bu formu silmek istediğinizden emin misiniz?');

    if (con) {
      //console.log('Silmek istediğiniz formun ID\'si: ' + formid);
      window.location.href = `detail/delete/${formid} `
      alert('silme başarılı')
    }
  }

  