try:
    import tiktoken
except ImportError:
    print("The 'tiktoken' module is not installed. Please install it using 'pip install tiktoken'.")
    exit(1)

# 사용할 모델 지정 (예: gpt-3.5-turbo)
model = "gpt-3.5-turbo"

# 텍스트 예제
text = """
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class Main {

    static int N, M;
    static int[][] map;
    static ArrayList<int[]> cctvs = new ArrayList<>();
    static int minArea = Integer.MAX_VALUE;
    static int[] dx = {0, 1, 0, -1};
    static int[] dy = {1, 0, -1, 0};

    static void find(int x, int y, int dir, int[][] tempMap) {
        int nx = x;
        int ny = y;

        while ((0 <= nx && nx < N && 0 <= ny && ny < M) && tempMap[nx][ny] != 6) {

            if (tempMap[nx][ny] == 0) {
                tempMap[nx][ny] = -1;
            }

            nx += dx[dir];
            ny += dy[dir];
        }
    }

    static int simulate() {
        int[][] tempMap = new int[N][M];
        for (int i = 0; i < N; i++) {
            tempMap[i] = map[i].clone();
        }

        for (int[] cc : cctvs) {
            int x = cc[0];
            int y = cc[1];
            int type = cc[2];
            int dir = cc[3];

            switch (type) {
                case 1:
                    find(x, y, dir, tempMap);
                    break;
                case 2:
                    find(x, y, dir, tempMap);
                    find(x, y, (dir + 2) % 4, tempMap);
                    break;
                case 3:
                    find(x, y, dir, tempMap);
                    find(x, y, (dir + 1) % 4, tempMap);
                    break;
                case 4:
                    find(x, y, dir, tempMap);
                    find(x, y, (dir + 1) % 4, tempMap);
                    find(x, y, (dir + 2) % 4, tempMap);
                    break;
                case 5:
                    find(x, y, dir, tempMap);
                    find(x, y, (dir + 1) % 4, tempMap);
                    find(x, y, (dir + 2) % 4, tempMap);
                    find(x, y, (dir + 3) % 4, tempMap);
                    break;
            }
        }

        int blind = 0;
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < M; j++) {
                if (tempMap[i][j] == 0) {
                    blind++;
                }
            }
        }

        return blind;
    }

    static void dfs(int index) {
        if (index == cctvs.size()) {
            minArea = Math.min(minArea, simulate());
            return;
        }

        int[] cctv = cctvs.get(index);
        int x = cctv[0];
        int y = cctv[1];
        int type = cctv[2];

        if (type == 5) {
            dfs(index + 1);
            return;
        }

        for (int dir = 0; dir < 4; dir++) {
            cctv[3] = dir;
            dfs(index + 1);
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] sp = br.readLine().split(" ");
        N = Integer.parseInt(sp[0]);
        M = Integer.parseInt(sp[1]);
        map = new int[N][M];
        for (int i = 0; i < N; i++) {
            sp = br.readLine().split(" ");
            for (int j = 0; j < M; j++) {
                map[i][j] = Integer.parseInt(sp[j]);
                int type = map[i][j];
                if (type >= 1 && type <= 5) {
                    cctvs.add(new int[]{i, j, type, 0});
                }
            }
        }

        dfs(0);

        System.out.println(minArea);
    }
}"""

# 모델에 맞는 인코딩 가져오기
encoding = tiktoken.encoding_for_model(model)

# 텍스트를 토큰화
tokens = encoding.encode(text)
print(f"Tokens: {tokens}")

# 토큰 수 계산
num_tokens = len(tokens)
print(f"Number of tokens: {num_tokens}")

# 토큰을 다시 텍스트로 디코딩
decoded_text = encoding.decode(tokens)
print(f"Decoded text: {decoded_text}")