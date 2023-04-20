# Singleton

A inteção do pattern *singleton* consiste em básicamente garantir que uma classe possua somente uma instância durante todo o ciclo de vida de uma aplicação assim como somente um ponto de acesso a essa instância. Um exemplo comum de uso desse pattern seria o de criação de um *pool de conexões* ou até mesmo um *gerenciador de configurações*.

A seguir, quatro maneiras de se aplicar um Singleton em Python.

#### Modo Tradicional

O modo tradicional de implementação desse pattern se baseia na criação de um método de classe responsável por garatir a existência de somente uma instância dessa classe.

```python
# modo_tradicional.py
class Singleton:
    _instance = None

    def __init__(self):
        self.some_attribute = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

Esse método é responsável por checar se já existe uma instância da classe `Singleton` e caso não exista, ele cria essa instância e retorna para o usuário, caso contrário, apenas retorna a instância já existente. O método *instance()* utiliza o pattern **Lazy Initialization** visto que a instância da classe será criada somente após o primeiro acesso.

```python
# Código de teste
from modo_tradicional import Singleton
foo = Singleton.instance()
bar = Singleton.instance()

print(foo is bar)
# True

foo.some_attribute = 'some value'

print(bar.some_attribute)
# 'some value'
```

#### Modo Simplificado

O modo mais simples de implementar o pattern singleton em python é a utilização de váriaveis de módulos, visto que os módulos python são carregados somente uma vez [¹]([6. Modules — Python 3.11.3 documentation](https://docs.python.org/3/tutorial/modules.html))(somente na primeira vez em que esse módulo for referenciado em um `import`).

```python
# modo_simplificado.py
class Singleton:

    def __init__(self):
        self.some_attribute = None


singleton = Singleton()

# Código de teste
from modo_simplificado import singleton
singleton.some_attribute = 'alegriaaa'
print(singleton.some_attribute)
# 'alegriaaa'
```

Repare que no código anterior, não foi necessário a criação do método *instance()*, pois iremos simplificar o uso do pattern através da variável `singleton` que está declarada no escopo do módulo `my_module.py`.

```python
# Código de teste
from modo_simplificado import singleton

foo = singleton
bar = singleton

print(foo is bar)
# True
foo.some_attribute = 'alo som a a'
print(bar.some_attribute)
# 'alo som a a'
```

Assim como a implementação, a utilização do pattern também passa a ser simplificada, porém com o mesmo efeito. Isso é possível graças ao fato de que os módulos do python funcionam como um objeto singleton.

#### Modo implícito

Uma forma de garantir que haverá somente uma instância de uma determinada classe é a utilização do método especial `__new__`. O método `__new__` é invocado pelo python sempre que uma nova instância de uma determinada classe for criada. O retorno desse método deverá ser a instância da classe em questão. Com isso, podemos transferir o mecanismo do método `instance()` para o método `__new__`.

```python
# modo_implicito.py
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

Como a inteligência do método `instance()` foi transferida para o método `__new__` o funcionamento basicamente é o mesmo, porém, a utilização da classe pode gerar confusões, já que não está mais explícito o fato de ser uma classe singleton.

```python
# Código de teste
from my_module import Singleton
foo = Singleton()
bar = Singleton()

print(foo is bar)
# True

foo.some_attribute = 'ô o carro do ovo'

print(bar.some_attribute)
# 'ô o carro do ovo'
```

#### Modo Genérico (para os exibidos)

Uma forma genérica e reaproveitável de implementar o pattern singleton é combinando-o com o pattern **Decorator** na criação de um mecanismo que se responsabilize por garantir a criação de uma instância única de qualquer classe.

```python
# modo_generico.py
def singleton(cls):
    instances = {}

    def instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return instance
```

Através de uma **Closure** o decorator de classe implementado no código anterior, define um mapeamento de instâncias tendo como chave as próprias classes.

```python
# outro_modulo.py
from my_decorators import singleton

@singleton
class Singleton:

    def __init__(self):
        self.some_attribute = None
```

Dessa forma, sempre que uma classe que esteja decorada como no exemplo anterior for instânciada, esse decorator garante a instância única.

```python
from outro_modulo import Singleton
foo = Singleton()
bar = Singleton()

print(foo is bar)
True

foo.some_attribute = 'ora ora eu mudei'

bar.some_attribute
print('ora ora eu mudei')
```

#### Algumas Considerações

- Como dito anteriormente, o python internamente utiliza o pattern singleton com certa frequência, não somente no mecanismo de modulos, mas também nos objetos `None`, `True` e `False`. Essa é a razão pela qual é considerada uma boa prática, sempre que testar se o valor de um objeto é `None`, utilizar o operador `is` ao invés do operador `==`.

- Em alguns casos, uma possível mudança de design onde uma classe que antes deveria se comportar como singleton e agora não mais, pode significar um problema, custando horas de refatoração para normalizar o código. Por essa razão, (assim como todos os outros) use esse pattern quando ele for realmente necessário.

- O mecanismo de módulo do python já é singleton, então, porque se preocupar em solucionar um problema já resolvido?

**Adaptado de: [Singleton - Python Design Patterns](https://design-patterns-ebook.readthedocs.io/en/latest/creational/singleton/)**
