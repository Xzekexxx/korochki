
class ImageSlider {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        this.slider = this.container.querySelector('.slider');
        this.slides = this.container.querySelectorAll('.slide');
        this.prevBtn = this.container.querySelector('.prev');
        this.nextBtn = this.container.querySelector('.next');
        this.dotsContainer = this.container.querySelector('.slider-dots');

        this.currentSlide = 0;
        this.slideCount = this.slides.length;
        this.autoPlayInterval = options.autoPlayInterval || 3000;
        this.isAutoPlaying = options.autoPlay !== false;

        this.touchStartX = 0;
        this.touchEndX = 0;

        this.init();
    }

    init() {
        if (this.slideCount === 0) return;

        this.createDots();

        this.showSlide(0);

        this.addEventListeners();

        if (this.isAutoPlaying) {
            this.startAutoPlay();
        }
    }

    createDots() {
        if (!this.dotsContainer) return;

        for (let i = 0; i < this.slideCount; i++) {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            dot.dataset.index = i;
            dot.addEventListener('click', () => this.goToSlide(i));
            this.dotsContainer.appendChild(dot);
        }
    }

    showSlide(index) {
        if (index < 0) index = this.slideCount - 1;
        if (index >= this.slideCount) index = 0;

        this.slider.style.transform = `translateX(-${index * 100}%)`;

        const dots = this.dotsContainer?.querySelectorAll('.dot');
        if (dots) {
            dots.forEach((dot, i) => {
                dot.classList.toggle('active', i === index);
            });
        }

        this.currentSlide = index;
    }

    nextSlide() {
        this.showSlide(this.currentSlide + 1);
    }

    prevSlide() {
        this.showSlide(this.currentSlide - 1);
    }

    goToSlide(index) {
        this.showSlide(index);
        this.resetAutoPlay();
    }

    startAutoPlay() {
        this.autoPlayTimer = setInterval(() => {
            this.nextSlide();
        }, this.autoPlayInterval);
    }

    stopAutoPlay() {
        if (this.autoPlayTimer) {
            clearInterval(this.autoPlayTimer);
        }
    }

    resetAutoPlay() {
        if (this.isAutoPlaying) {
            this.stopAutoPlay();
            this.startAutoPlay();
        }
    }

    addEventListeners() {

        this.prevBtn?.addEventListener('click', () => {
            this.prevSlide();
            this.resetAutoPlay();
        });

        this.nextBtn?.addEventListener('click', () => {
            this.nextSlide();
            this.resetAutoPlay();
        });

        this.container.addEventListener('touchstart', (e) => {
            this.touchStartX = e.changedTouches[0].screenX;
        });

        this.container.addEventListener('touchend', (e) => {
            this.touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe();
        });

        this.container.addEventListener('mouseenter', () => {
            if (this.isAutoPlaying) {
                this.stopAutoPlay();
            }
        });

        this.container.addEventListener('mouseleave', () => {
            if (this.isAutoPlaying) {
                this.startAutoPlay();
            }
        });
    }

    handleSwipe() {
        const swipeThreshold = 50;
        const diff = this.touchEndX - this.touchStartX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                this.prevSlide(); 
            } else {
                this.nextSlide(); 
            }
            this.resetAutoPlay();
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const sliderElement = document.getElementById('main-slider');
    if (sliderElement) {
        new ImageSlider('main-slider', {
            autoPlayInterval: 3000,
            autoPlay: true
        });
    }
});
