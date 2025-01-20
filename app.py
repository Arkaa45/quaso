from flask import Flask, render_template, request
import math

app = Flask(__name__)

def poisson_probability(lmbda, k):
    """
    Menghitung probabilitas distribusi Poisson untuk P(X = k).
    """
    return (lmbda ** k) * math.exp(-lmbda) / math.factorial(k)

def poisson_cumulative_probability(lmbda, k):
    """
    Menghitung probabilitas kumulatif distribusi Poisson untuk P(X <= k).
    """
    cumulative_prob = sum((lmbda ** i) * math.exp(-lmbda) / math.factorial(i) for i in range(k + 1))
    return cumulative_prob

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    cumulative = None
    explanation = None
    if request.method == 'POST':
        try:
            # Ambil input dari form
            lmbda = float(request.form['lambda'])  # Input rata-rata paket (λ)
            k = int(request.form['k'])  # Input jumlah paket (k)

            # Hitung probabilitas P(X = k)
            result = poisson_probability(lmbda, k)

            # Jika kumulatif dipilih, hitung P(X <= k)
            if 'cumulative' in request.form:
                cumulative = poisson_cumulative_probability(lmbda, k)

            # Buat penjelasan hasil
            explanation = f"""
                Berdasarkan rata-rata pengantaran paket sebesar {lmbda} paket per hari (λ),
                probabilitas bahwa jumlah paket yang tepat diantar pada hari tertentu adalah {k} dihitung menggunakan
                distribusi Poisson. Rumus yang digunakan adalah:
                
                P(X = k) = (λ^k * e^(-λ)) / k!
                
                Jika probabilitas kumulatif dihitung, maka P(X ≤ k) mencakup semua probabilitas
                dari pengantaran 0 hingga {k} paket pada hari tertentu.
                
                Studi kasus ini membantu ekspedisi memperkirakan jumlah pengiriman yang mungkin terjadi pada hari tertentu
                untuk tujuan perencanaan logistik dan sumber daya.
            """
        except (ValueError, OverflowError):
            # Tangani error input
            result = "Input tidak valid! Mohon masukkan angka yang sesuai."
            cumulative = None
            explanation = None

    return render_template('index.html', result=result, cumulative=cumulative, explanation=explanation)

if __name__ == '__main__':
    app.run(debug=True)
