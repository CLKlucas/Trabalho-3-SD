import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TopcarClient {
    private static final String BASE_URL = System.getenv().getOrDefault(
            "TOPCAR_API_URL",
            "http://localhost:8000/api");

    private static final HttpClient CLIENT = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_1_1)
            .build();

    public static void main(String[] args) throws Exception {
        show("Operacoes", call("GET", "/operacoes", null));
        show("Pecas", call("GET", "/pecas", null));
        show("Peca 1", call("GET", "/pecas/1", null));

        String clienteJson = "{\"cpf\":\"11122233344\",\"nome\":\"Cliente Java\",\"idade\":23}";
        show("Cadastrar cliente", call("POST", "/clientes", clienteJson));

        String pedidoJson = "{\"cpf\":\"11122233344\",\"itens\":["
                + "{\"pecaId\":1,\"quantidade\":2,\"descontoPercentual\":5},"
                + "{\"pecaId\":3,\"quantidade\":1}]}";
        HttpResponse<String> pedidoResponse = call("POST", "/pedidos", pedidoJson);
        show("Criar pedido", pedidoResponse);

        int pedidoId = extractPedidoId(pedidoResponse.body());
        show("Total pedido " + pedidoId, call("GET", "/pedidos/" + pedidoId + "/total", null));
        show("Consultar cliente", call("GET", "/clientes/11122233344", null));
    }

    private static HttpResponse<String> call(String method, String path, String body)
            throws IOException, InterruptedException {
        HttpRequest.Builder builder = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + path))
                .version(HttpClient.Version.HTTP_1_1)
                .header("Accept", "application/json");

        if ("POST".equalsIgnoreCase(method)) {
            builder.header("Content-Type", "application/json");
            builder.POST(HttpRequest.BodyPublishers.ofString(body));
        } else {
            builder.GET();
        }

        return CLIENT.send(builder.build(), HttpResponse.BodyHandlers.ofString());
    }

    private static void show(String title, HttpResponse<String> response) {
        System.out.println();
        System.out.println(title + " - HTTP " + response.statusCode());
        System.out.println(response.body());
    }

    private static int extractPedidoId(String body) {
        Pattern pattern = Pattern.compile("\"pedido\"\\s*:\\s*\\{\\s*\"id\"\\s*:\\s*(\\d+)");
        Matcher matcher = pattern.matcher(body);
        if (!matcher.find()) {
            throw new IllegalStateException("Nao foi possivel localizar o id do pedido na resposta: " + body);
        }
        return Integer.parseInt(matcher.group(1));
    }
}
