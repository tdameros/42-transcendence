export class BootstrapUtils {
  static setInvalidInput(input) {
    input.classList.remove('is-valid');
    input.classList.add('is-invalid');
  }

  static setValidInput(input) {
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
  }
}
