
const redirectToCode = (code) => {
	window.location.assign(`/${code}`)
}
const checkCode = (code) => {
	fetch("/check", {
        method: 'POST',
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
            key : code,
        }),
    })
    .then(response => response.json())
    .then(json => {
		if (json.found) {
			$('#found').removeClass("d-none");
			redirectToCode(code)
		} else {
			$('#not-found').removeClass("d-none");
		}
	})
}
$('.digit-group').find('input').each(function() {
	$(this).attr('maxlength', 1);
	$(this).on('keyup', function(e) {
		var parent = $($(this).parent());
		$('#found').addClass("d-none");
		$('#not-found').addClass("d-none");

		if(e.keyCode === 8 || e.keyCode === 37) {
			var prev = parent.find('input#' + $(this).data('previous'));
			
			if(prev.length) {
				$(prev).select();
			}
		} else if((e.keyCode >= 48 && e.keyCode <= 57) || (e.keyCode >= 65 && e.keyCode <= 90) || (e.keyCode >= 96 && e.keyCode <= 105) || e.keyCode === 39) {
			var next = parent.find('input#' + $(this).data('next'));
			if(next.length) {
				$(next).select();
			} else {
				if(parent.data('autosubmit')) {
					parent.submit();
				}				
				var code = ($('#digit-1').val() || "") + ($('#digit-2').val() || "") + ($('#digit-3').val() || "") + ($('#digit-4').val() || "");
				checkCode(code)
			}
		}
	});
});