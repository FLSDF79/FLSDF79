# Threat model da skill

## Escopo

Este documento define os riscos mínimos para qualquer skill publicada neste repositório. A implementação funcional ainda não foi definida; portanto, nenhum domínio, ferramenta, segredo, fluxo de publicação ou integração é considerado permitido por padrão.

## Ativos a proteger

Os ativos incluem prompts internos, instruções da skill, credenciais, tokens, cookies, variáveis de ambiente, dados pessoais, dados bancários, informações institucionais, memória persistente, arquivos do usuário, resultados de ferramentas, código de terceiros e capacidade de executar ações externas.

## Fronteiras de confiança

| Fonte | Classificação | Regra |
|---|---|---|
| Instruções de sistema e políticas de segurança | Confiável superior | Não podem ser substituídas por conteúdo externo |
| Código da skill revisado e protegido por branch | Confiável condicionado | Deve passar por revisão e CI |
| Usuário autenticado | Confiável condicionado | Continua sujeito a confirmação para ações irreversíveis |
| Arquivos, URLs, PDFs, imagens e planilhas | Não confiável | Dados para análise; nunca instruções privilegiadas |
| Issues, pull requests e comentários | Não confiável | Podem conter prompt injection indireto |
| Resultados de APIs e ferramentas | Não confiável | Validar proveniência e schema antes de reutilizar |
| Memória recuperada | Não confiável por padrão | Não transformar automaticamente em regra persistente |

## Cenários de ameaça

| ID | Ameaça | Impacto | Controle obrigatório |
|---|---|---|---|
| PI-001 | Conteúdo ordena ignorar instruções anteriores | Perda de controle do agente | Separação entre instruções e dados; classificação e falha segura |
| PI-002 | Documento pede revelação de prompt, memória ou token | Exfiltração | Redação, bloqueio server-side e proibição de acesso a secrets |
| PI-003 | Página ou issue pede chamada a webhook | Vazamento de dados | Allowlist de destinos e confirmação humana |
| PI-004 | PDF, imagem ou planilha contém instrução oculta | Execução indireta | OCR/análise como dado não confiável e testes multimodais |
| PI-005 | Resultado de ferramenta tenta influenciar a próxima ferramenta | Escalada de privilégio | Etapas isoladas, schema fechado e gateway de ferramentas |
| PI-006 | Pull request usa workflow privilegiado | Comprometimento da CI | `pull_request`, permissões de leitura e ausência de secrets em forks |
| PI-007 | Dependência ou action mutável é comprometida | Supply chain | SHA pinning, allowlist e Dependabot |
| PI-008 | Skill grava instrução maliciosa na memória | Persistência | Memória separada, expiração e aprovação humana |
| PI-009 | SSRF ou exfiltração por URL | Acesso indevido | Allowlist, bloqueio de redes privadas e limites de resposta |
| PI-010 | Ação irreversível executada sem consentimento | Dano operacional | Gate de confirmação, idempotência e trilha de auditoria |

## Regras de autorização

O modelo pode classificar conteúdo e propor uma ação, mas nunca concede a própria autorização. A aplicação deve controlar o usuário, o alvo, o domínio, a ferramenta, o tipo de operação, o limite de dados e a necessidade de confirmação. Shell arbitrário, leitura de variáveis de ambiente, publicação, exclusão, alteração de permissões, upload e envio externo devem ser negados por padrão.

## Critérios de segurança

Uma versão somente pode ser considerada candidata a publicação quando não houver segredo no diff ou histórico do branch, os testes de prompt injection passarem, as chamadas de ferramentas forem bloqueadas nos casos maliciosos, as saídas estiverem redigidas, o workflow usar permissões mínimas e uma revisão humana confirmar o escopo funcional.

> Ausência de uma detecção textual não prova ausência de prompt injection. A defesa principal deve estar na separação de privilégios e na autorização server-side.
