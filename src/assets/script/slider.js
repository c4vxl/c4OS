class Slider {
    constructor(element, slides = [], supressNextButtonHandler = false, supressPrevButtonHandler = false) {
        this.slidesContainer = element.querySelector(":scope .slide__container");
        slides.forEach(s => this.slidesContainer.innerHTML += s);
        this.slides = this.slidesContainer.querySelectorAll(".slide");
        this.nextBtn = element.querySelector(":scope > .slide__indicator .next");
        this.prevBtn = element.querySelector(":scope > .slide__indicator .prev");
        this.current = 0;
        this.slides.forEach(s => element.querySelector(":scope > .slide__indicator .circle__container").innerHTML += `<div class="circle"></div>`);
        this.circles = element.querySelectorAll(":scope > .slide__indicator .circle__container .circle");

        if (!supressNextButtonHandler) this.nextBtn?.addEventListener("click", () => this.display(this.current + 1));
        if (!supressPrevButtonHandler) this.prevBtn?.addEventListener("click", () => this.display(this.current - 1));

        this.slides[0]?.classList?.add("active");
        this.offset = (element.offsetWidth / 2) - (this.slides[0].offsetWidth / 2);
        this.display(0);
    }

    display(n) {
        n = n >= 0 ? n : this.slides.length - 1;
        n = n < this.slides.length ? n : 0;
        this.current = n;

        [...this.slides, ...this.circles].forEach(e => e.classList.remove("active"));
        [this.slides[n], this.circles[n]].forEach(e => e.classList.add("active"));
        this.slidesContainer.style.transform = `translateX(${this.offset - (n * (this.slides[n].offsetWidth + 5))}px)`;
    }
}