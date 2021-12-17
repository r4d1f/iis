using System;
using System.Threading;

namespace IoC
{
    public interface IAlgorithm
    {
        bool Hash();
    }

    public class SHA256 : IAlgorithm
    {
        public bool Hash()
        {
            var guid = Guid.NewGuid();
            Thread.Sleep(1000);
            var hash = guid.GetHashCode();
            if (hash <= 10000)
            {
                return true;
            }

            return false;

        }

        public override string ToString()
        {
            return nameof(SHA256);
        }
    }

    public class Ethash : IAlgorithm
    {
        public bool Hash()
        {
            var random = new Random();
            Thread.Sleep(1000);
            var hash = random.Next(30000);
            if (hash <= 10000)
            {
                return true;
            }

            return false;
        }

        public override string ToString()
        {
            return nameof(Ethash);
        }
    }

    public class Miner
    {
        private IAlgorithm algoritm;

        private Thread thread;

        public event EventHandler<bool> HashFound;

        public Miner(IAlgorithm algorithm)
        {
            algoritm = algorithm;
            thread = new Thread(Mine);
        }

        public void Start()
        {
            thread.Start();
        }

        public void Stop()
        {
            thread.Abort();
        }

        private void Mine()
        {
            while (true)
            {
                var hashResult = algoritm.Hash();
                HashFound?.Invoke(this, hashResult);
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Miner miner = null;
            Console.WriteLine("Выберите алгоритм: ");
            Console.WriteLine("1 - SHA256");
            Console.WriteLine("2 - Ethash");
            var algorithmImput = Console.ReadLine();
            if (int.TryParse(algorithmImput, out int algorithm))
            {
                switch (algorithm)
                {
                    case 1:
                        miner = new Miner(new SHA256());
                        break;
                    case 2:
                        miner = new Miner(new Ethash());
                        break;
                    default:
                        throw new ArgumentException("Неизвестный алгоритм.", nameof(algorithm));
                }
            }

            miner.HashFound += Miner_HashFound;

            Console.WriteLine($"Начало {DateTime.Now.ToShortTimeString()}");
            miner.Start();
        }

        private static void Miner_HashFound(object sender, bool e)
        {
            if (e)
            {
                Console.WriteLine("хеш найден");
            }
            else
            {
                Console.WriteLine("Некорректный хеш");
            }
        }
    }
}
