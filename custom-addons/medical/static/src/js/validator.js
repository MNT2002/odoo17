function Validator(formSelector, options = {}) {
  function getParent(element, selector) {
    while (element.parentElement) {
      if (element.parentElement.matches(selector)) {
        return element.parentElement;
      }
      element = element.parentElement;
    }
  }

  var formRules = {};

  var validatorRules = {
    required: function (value) {
      return value ? undefined : "Vui lòng nhập trường này";
    },
    email: function (value) {
      var regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
      return regex.test(value)
        ? undefined
        : "Vui lòng nhập đúng định dạng email";
    },
    phone: function (value) {
      // var phoneno = /^\+?([0-9]{2})\)?[-. ]?([0-9]{4})[-. ]?([0-9]{4})$/;
      var phoneno = /^(0|\+84)[1-9]\d{8}$/;
      return value.match(phoneno)
      ? undefined
      : "Vui lòng nhập đúng định dạng số điện thoại"
    },
    min: function (min) {
      return function (value) {
        return value.length >= min
          ? undefined
          : `Vui lòng nhập ít nhất ${min} kí tự`;
      };
    },
  };

  formElement = document.querySelector(formSelector);

  if (formElement) {
    var inputs = formElement.querySelectorAll("[name][rules]");

    for (var input of inputs) {
      var rules = input.getAttribute("rules").split("|");
      for (var rule of rules) {
        var ruleInfo;
        var isRuleHasValue = rule.includes(":");

        if (isRuleHasValue) {
          ruleInfo = rule.split(":");
          rule = ruleInfo[0];
        }

        var ruleFunc = validatorRules[rule];

        if (isRuleHasValue) {
          ruleFunc = ruleFunc(ruleInfo[1]);
        }

        // console.log(rule)

        if (Array.isArray(formRules[input.name])) {
          formRules[input.name].push(ruleFunc);
        } else {
          formRules[input.name] = [ruleFunc];
        }
      }

      input.onblur = handleValidate;
      input.oninput = handleClearError;
    }

    function handleValidate(e) {
      var rules = formRules[e.target.name];

      var errorMessage;

      rules.find(function (rule) {
        errorMessage = rule(e.target.value);
        return errorMessage;
      });

      if (errorMessage) {
        var formGroup = getParent(e.target, ".form-group");
        if (formGroup) {
          formGroup.classList.add("invalid");
          var formMessage = formGroup.querySelector(".form-message");
          if (formMessage) {
            formMessage.innerText = errorMessage;
          }
        }
      }

      return !errorMessage;
    }

    function handleClearError(e) {
      var formGroup = getParent(e.target, ".form-group");
      if (formGroup.classList.contains("invalid")) {
        formGroup.classList.remove("invalid");
        var formMessage = formGroup.querySelector(".form-message");
        if (formMessage) {
          formMessage.innerText = "";
        }
      }
    }

    formElement.onsubmit = function (e) {
      e.preventDefault();
      var inputs = formElement.querySelectorAll("[name][rules]");
      var isValid = true;

      for (var input of inputs) {
        if (!handleValidate({ target: input })) {
          isValid = false;
        }
      }

      if (isValid) {
        if (typeof options.onSubmit === "function") {
          var enableInputs = formElement.querySelectorAll("[name]");
          var formValues = Array.from(enableInputs).reduce(function (values,input) {
            // convert formValues từ nodeList  sang 1 array

            switch (input.type) {
              case "checkbox":
                if (!input.matches(":checked")) {
                  values[input.name] = "";
                  return values; // Nếu kiểm tra input ko được checked thì return luôn
                }
                if (!Array.isArray(values[input.name])) {
                  // kiểm tra nếu values[input.name] không phải là mảng
                  values[input.name] = [];
                }

                values[input.name].push(input.value);

                break;
              case "radio":
                values[input.name] = formElement.querySelector(
                  'input[name="' + input.name + '"]:checked'
                ).value; // trả về value của radio checked
                break;
              case "file":
                values[input.name] = input.files;
                break;

              default:
                values[input.name] = input.value; // gán các key của object trả về là input.name có giá trị là input.value (giá trị nhập vào ô input)
            }
            return values;
          },
          {}); // gán giá trị mặc định của hàm reduce() là 1 object

          options.onSubmit(formValues);
        } else {
          formElement.submit();
        }
      }
    };
    // console.log(formRules)
  }
}
