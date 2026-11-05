# open-finance-specs

Fonte da verdade interna das specs Open Finance Brasil (Current/Deprecated), fixadas por commit e SHA-256, com catálogo e PCM.

Os projetos consomem as specs daqui, por commit fixado. Ninguém edita um arquivo de spec: uma versão nova entra como um arquivo novo, com novo hash no catálogo.

## O que tem aqui

| Caminho | Conteúdo |
|---|---|
| `contracts/expansion/catalog.json` | Catálogo: 35 contratos ativos e 143 operações, com domínio, versão, URL de origem, commit, SHA-256 e cada operação. |
| `contracts/expansion/snapshots/` | Os 35 arquivos OpenAPI oficiais, sem nenhuma alteração. |
| `contracts/expansion/sources/` | A tabela oficial de versões do portal. |
| `contracts/expansion/verify_catalog.py` | Verificação de integridade, sem rede. |
| `contracts/reporting/pcm/` | OpenAPI da PCM, política e proveniência. |
| `contracts/open-finance/` e `contracts/manifest.json` | Os quatro contratos da primeira POC, preservados. |

## Corte

- **Data-base do catálogo:** 25/10/2026. Não é atualizado sozinho: as versões oficiais mudam depois disso.
- **Origem desta cópia:** `leonidasleme/openfinance`, commit `b6bb8134203cc144d8ec934c642f656a835629e3` (`labs/exposure-engine/contracts` e `contracts`).
- **Escopo:** versões `Current` e `Deprecated` do Open Finance Brasil. Open Insurance fica de fora. No corte não há nenhuma `Deprecated`.
- **Candidatas:** versões em implantação ou certificação não entram na cobertura ativa. Por isso `loans-2.7.0` existe em `contracts/open-finance/`, mas a versão ativa é a 2.6.0.

O catálogo prova que os arquivos foram preservados e que as operações foram listadas. Ele não diz quais APIs a XP é obrigada a atender.

## Verificar

```bash
pip install pyyaml
python contracts/expansion/verify_catalog.py
```

Saída esperada: `PASS: 35 active contracts, 143 unique operations, 5 source hashes, 4 legacy snapshots unchanged.`

O `.gitattributes` marca `contracts/**` com `-text`: os hashes valem para os bytes exatos, então o Git não pode normalizar o fim de linha.
