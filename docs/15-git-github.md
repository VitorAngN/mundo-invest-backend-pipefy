# Git e GitHub

## Estado local

Branch:

```text
codex/mundo-invest-backend
```

Commits locais:

```text
09e8f32 Add CI workflow for tests
73ac651 Implement client management Pipefy API
```

## Criar repositorio remoto

Como o GitHub CLI (`gh`) nao esta instalado neste computador, o caminho mais simples e criar o repositorio pelo navegador.

Sugestao de nome:

```text
mundo-invest-backend-pipefy
```

No GitHub:

1. Clique em `New repository`.
2. Use o nome sugerido.
3. Deixe publico ou privado conforme a regra do teste.
4. Nao crie README pelo GitHub, porque o projeto local ja tem README.
5. Crie o repositorio.

## Adicionar remote

Depois de criar o repo, rode na raiz do projeto:

```powershell
git remote add origin https://github.com/SEU_USUARIO/mundo-invest-backend-pipefy.git
```

Conferir:

```powershell
git remote -v
```

## Push

```powershell
git push -u origin codex/mundo-invest-backend
```

Se quiser que a branch principal do GitHub seja `main`, depois pode abrir PR ou renomear a branch pelo GitHub. Para o teste, enviar o link da branch/repo ja costuma ser suficiente, desde que o avaliador consiga ver o codigo.

## Conferencia antes de enviar

No GitHub, confira:

- README renderizando corretamente;
- pasta `app/` presente;
- pasta `tests/` presente;
- pasta `docs/` presente;
- workflow de Actions em `.github/workflows/tests.yml`;
- Actions passando.

