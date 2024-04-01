<section class="call-to-action-section">
    <div class="container">
        <h2>Ready to Cultivate Your Future?</h2>
        <a href="/signup" class="btn btn-lg btn-wheat">Get Growing Today</a>
    </div>
</section>

<style>
    .call-to-action-section {
        background-image: url('https://source.unsplash.com/random/1920x1080/?farm,field');
        background-size: cover;
        background-position: center;
        color: #fff;
        padding: 80px 0;
        text-align: center;
        position: relative;
    }

    .call-to-action-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(46, 104, 14, 0.8);
    }

    .call-to-action-section .container {
        position: relative;
        z-index: 1;
    }

    .call-to-action-section h2 {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 40px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }

    .call-to-action-section .btn {
        font-size: 1.5rem;
        padding: 15px 30px;
        background-color: #f5d142;
        color: #333;
        border: none;
        border-radius: 4px;
        box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        transition: background-color 0.3s ease;
    }

    .call-to-action-section .btn:hover {
        background-color: #e0c028;
    }
</style>