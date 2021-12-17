using System;
using System.Threading;

namespace DefaultApp
{
    public class Miner
    {

        private SHA256 sha256;

        private Thread thread;

        //Observer
        public event EventHandler<bool> HashFound;

        public Miner()
        {
            sha256 = new SHA256();
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
                var hashResult = sha256.Hash();
                HashFound?.Invoke(this, hashResult);
            }
        }
    }

    public class SHA256
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

    class Program
    {
        static void Main(string[] args)
        {
            var miner = new Miner();

            miner.HashFound += Miner_HashFound;

            Console.WriteLine($"Начало: {DateTime.Now.ToShortTimeString()}");
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
